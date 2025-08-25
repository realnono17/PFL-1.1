# Revised country_multiplier.py using country codes

country_multiplier = {
    # 🔥 Top-Tier (1.25)
    208: 1.25,  # France
    210: 1.25,  # Germany
    215: 1.25,  # Italy
    236: 1.25,  # Spain
    204: 1.25,  # England
    146: 1.25,  # Brazil
    144: 1.25,  # Argentina

    # 💸 High-Tier (1.15)
    228: 1.15,  # Portugal
    224: 1.15,  # Netherlands
    197: 1.15,  # Belgium
    152: 1.15,  # Uruguay
    148: 1.15,  # Colombia
    124: 1.15,  # Mexico
    200: 1.15,  # Croatia
    135: 1.15,  # United States
    13:  1.15,  # Japan
    190: 1.15,  # Turkey

    # ⚖️ Mid-Tier (1.05)
    194: 1.05,  # Austria
    238: 1.05,  # Switzerland
    227: 1.05,  # Poland
    303: 1.05,  # Serbia
    203: 1.05,  # Denmark
    230: 1.05,  # Russia
    226: 1.05,  # Norway
    237: 1.05,  # Sweden
    16:  1.05,  # South Korea
    147: 1.05,  # Chile
    150: 1.05,  # Paraguay
    151: 1.05,  # Peru
    232: 1.05,  # Scotland
    239: 1.05,  # Ukraine
    7:   1.05,  # China
    162: 1.05,  # Australia

    # 🟨 Low-Tier (0.95)
    211: 0.95,  # Greece
    229: 0.95,  # Romania
    202: 0.95,  # Czech Republic
    234: 0.95,  # Slovakia
    212: 0.95,  # Hungary
    44:  0.95,  # Algeria
    58:  0.95,  # Egypt
    87:  0.95,  # South Africa
    110: 0.95,  # Canada
    76:  0.95,  # Morocco
    80:  0.95,  # Nigeria
    64:  0.95,  # Ghana
    50:  0.95,  # Cameroon
    189: 0.95,  # Israel

    # 🧪 Unknown/Underrated (0.90)
    9:   0.90,  # India
    38:  0.90,  # Vietnam
    36:  0.90,  # Thailand
    21:  0.90,  # Malaysia
    11:  0.90,  # Iran
    12:  0.90,  # Iraq
    37:  0.90,  # UAE
    30:  0.90,  # Qatar
    10:  0.90,  # Indonesia
    31:  0.90,  # Saudi Arabia
    166: 0.90,  # New Zealand

    # 🧊 Low Exposure/Non-competitive (0.80)
    192: 0.80,  # Andorra
    221: 0.80,  # San Marino
    231: 0.80,  # San Marino (duplicate entry)
    218: 0.80,  # Liechtenstein
    220: 0.80,  # Luxembourg
    245: 0.80,  # Gibraltar

    # Afghanistan (multiple codes mapped to 0.80)
    1:   0.80,
    35:  0.80,
    96:  0.80,
    97:  0.80,
    99:  0.80,
    101: 0.80,
    102: 0.80,
    141: 0.80,
    142: 0.80,
    143: 0.80,
    154: 0.80,
    155: 0.80,
    156: 0.80,
    157: 0.80,
    158: 0.80,
    160: 0.80,
    173: 0.80,
    174: 0.80,
    175: 0.80,
    177: 0.80,
    178: 0.80,
    179: 0.80,
    180: 0.80,
    181: 0.80,
    182: 0.80,
    183: 0.80,
    185: 0.80,
    186: 0.80,
    187: 0.80,
    188: 0.80,
    242: 0.80,
    243: 0.80,
    244: 0.80,
    246: 0.80,
    247: 0.80,
    248: 0.80,
    252: 0.80,
    253: 0.80,
    254: 0.80,
    255: 0.80,
    256: 0.80,
    257: 0.80,
    258: 0.80,
    259: 0.80,
    
    # Low Exposure continued
    4:   0.80,  # Bhutan
    25:  0.80,  # Nepal
    3:   0.80,  # Bangladesh
    27:  0.80,  # Pakistan
    222: 0.80,  # Malta
    311: 0.80,  # Kosovo
    15:  0.80,  # North Korea

    # Fallback multiplier for any country code not listed
    "default": 1.00,
}
