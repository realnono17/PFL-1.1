from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import httpx, os
from urllib.parse import urlencode
from app.database import get_db
from app.models.user import User
from app.models.club import Club
from app.utils.auth_utils import create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

CLIENT_ID = os.getenv("DISCORD_CLIENT_ID")
CLIENT_SECRET = os.getenv("DISCORD_CLIENT_SECRET")
REDIRECT_URI = os.getenv("DISCORD_REDIRECT_URI")
GUILD_ID = os.getenv("DISCORD_GUILD_ID")
BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")


@router.get("/discord_login")
def discord_login():
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": "identify guilds guilds.members.read"
    }
    return RedirectResponse(f"https://discord.com/api/oauth2/authorize?{urlencode(params)}")


@router.get("/callback")
async def discord_callback(code: str, db: Session = Depends(get_db)):
    async with httpx.AsyncClient() as client:
        # 1. Exchange code for token
        token_res = await client.post("https://discord.com/api/oauth2/token", data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI
        }, headers={"Content-Type": "application/x-www-form-urlencoded"})

        if token_res.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to exchange token")

        token_data = token_res.json()
        access_token = token_data["access_token"]

        # 2. Get user info
        user_res = await client.get("https://discord.com/api/users/@me", headers={
            "Authorization": f"Bearer {access_token}"
        })
        user = user_res.json()

        # 3. Get member roles in your guild
        guild_res = await client.get(f"https://discord.com/api/users/@me/guilds/{GUILD_ID}/member", headers={
            "Authorization": f"Bearer {access_token}"
        })

        if guild_res.status_code != 200:
            raise HTTPException(status_code=403, detail="User not in guild")

        member_data = guild_res.json()
        role_ids = member_data["roles"]

        # 4. Get full role list from the bot
        role_res = await client.get(f"https://discord.com/api/guilds/{GUILD_ID}/roles", headers={
            "Authorization": f"Bot {BOT_TOKEN}"
        })
        role_map = {r["id"]: r["name"] for r in role_res.json()}

        # 5. Detect club role
        club_name = None
        for rid in role_ids:
            if rid in role_map:
                club_name = role_map[rid]  # e.g. "ReTest1", "Barcelona", etc.
                break

        if not club_name:
            raise HTTPException(status_code=403, detail="No valid club role found")

        # 6. Match club in DB
        club = db.query(Club).filter_by(name=club_name).first()
        if not club:
            raise HTTPException(status_code=404, detail=f"Club '{club_name}' not found")

        # 7. Upsert user
        discord_id = user["id"]
        username = user["username"]

        db_user = db.query(User).filter_by(discord_id=discord_id).first()
        if not db_user:
            db_user = User(
                discord_id=discord_id,
                username=username,
                role="manager",
                club_id=club.id
            )
            db.add(db_user)
            db.commit()
            db.refresh(db_user)

        # 8. Create JWT token
        token = create_access_token({
            "user_id": db_user.id,
            "role": db_user.role,
            "club_id": db_user.club_id
        })

        return {"access_token": token, "token_type": "bearer"}
