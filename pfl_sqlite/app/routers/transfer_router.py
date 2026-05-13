from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.models.transfer import Transfer
from app.models.player import Player
from app.models.club import Club
from app.models.financial_log import FinancialLog
from app.schemas.transfer_schema import TransferCreate, TransferUpdate, TransferOut
from app.database import get_db
from app.dependencies import require_admin

router = APIRouter(prefix="/transfers", tags=["Transfers"])


@router.get("/", response_model=List[TransferOut])
def get_transfers(db: Session = Depends(get_db)):
    return db.query(Transfer).all()


@router.get("/{transfer_id}", response_model=TransferOut)
def get_transfer(transfer_id: int, db: Session = Depends(get_db)):
    transfer = db.query(Transfer).get(transfer_id)
    if not transfer:
        raise HTTPException(status_code=404, detail="Transfer not found")
    return transfer


@router.post("/", response_model=TransferOut)
def create_transfer(transfer: TransferCreate, db: Session = Depends(get_db)):
    player = db.query(Player).filter(Player.id == transfer.player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    to_club = db.query(Club).get(transfer.to_club_id)
    if not to_club:
        raise HTTPException(status_code=404, detail="Destination club not found")

    from_club = db.query(Club).get(transfer.from_club_id) if transfer.from_club_id else None

    # Deduct budgets for to_club
    if transfer.transfer_fee:
        to_club.transfer_budget -= transfer.transfer_fee
    if player.wage:
        to_club.wage_budget -= player.wage

    # Update player's club
    player.club_id = transfer.to_club_id

    # Create Transfer record
    db_transfer = Transfer(**transfer.model_dump())
    db.add(db_transfer)

    # Log outgoing for destination club
    if transfer.transfer_fee:
        db.add(FinancialLog(
            club_id=to_club.id,
            amount=-transfer.transfer_fee,
            type="transfer",
            description=f"Bought {player.name} from {from_club.name if from_club else 'Unknown'} for €{int(transfer.transfer_fee):,}"
        ))

    if player.wage:
        db.add(FinancialLog(
            club_id=to_club.id,
            amount=-player.wage,
            type="wage",
            description=f"Signed {player.name} with wage €{int(player.wage):,}"
        ))

    # Log income for seller club
    if from_club:
        if transfer.transfer_fee:
            db.add(FinancialLog(
                club_id=from_club.id,
                amount=transfer.transfer_fee,
                type="transfer_income",
                description=f"Sold {player.name} to {to_club.name} for €{int(transfer.transfer_fee):,}"
            ))

        if player.wage:
            db.add(FinancialLog(
                club_id=from_club.id,
                amount=player.wage,
                type="wage_relief",
                description=f"Released {player.name}, saving wage of €{int(player.wage):,}"
            ))

    # Finalize
    db.commit()
    db.refresh(db_transfer)
    return db_transfer

@router.put("/{transfer_id}", response_model=TransferOut, dependencies=[Depends(require_admin)])
def update_transfer(transfer_id: int, transfer: TransferUpdate, db: Session = Depends(get_db)):
    db_transfer = db.query(Transfer).get(transfer_id)
    if not db_transfer:
        raise HTTPException(status_code=404, detail="Transfer not found")
    for key, value in transfer.model_dump().items():
        setattr(db_transfer, key, value)
    db.commit()
    db.refresh(db_transfer)
    return db_transfer


@router.delete("/{transfer_id}", dependencies=[Depends(require_admin)])
def delete_transfer(transfer_id: int, db: Session = Depends(get_db)):
    db_transfer = db.query(Transfer).get(transfer_id)
    if not db_transfer:
        raise HTTPException(status_code=404, detail="Transfer not found")
    db.delete(db_transfer)
    db.commit()
    return {"detail": f"Transfer {transfer_id} deleted"}
