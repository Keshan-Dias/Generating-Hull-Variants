import math

def holtrop_resistance_power(
    L, B, T, CB, V_knots,
    rho=1025.0, nu=1.19e-6, g=9.81,
    eta_D=0.715
):
    """
    Holtrop–Mennen calm-water resistance and power prediction
    with detailed resistance component breakdown.
    """

    # --------------------------------------------------
    # Speed & displacement
    # --------------------------------------------------
    V_ms = V_knots * 0.5144
    disp_volume = L * B * T * CB

    # --------------------------------------------------
    # Wetted surface area (Holtrop)
    # --------------------------------------------------
    S = L * (2 * T + B) * math.sqrt(CB) * (
        0.453
        + 0.4425 * CB
        - 0.2862 * CB**2
        + 0.003467 * (B / T)
    )

    # --------------------------------------------------
    # Form factor (1 + k)
    # --------------------------------------------------
    one_plus_k = (
        0.93
        + 0.487 * (B / T) ** 1.068
        * (L / B) ** -0.461
        * (L / T) ** 0.121
    )
    k = one_plus_k - 1.0

    # --------------------------------------------------
    # Frictional resistance (ITTC-1957)
    # --------------------------------------------------
    Re = (V_ms * L) / nu
    Cf = 0.075 / ((math.log10(Re) - 2) ** 2)
    Rf = 0.5 * rho * V_ms**2 * S * Cf

    # --------------------------------------------------
    # Form resistance
    # --------------------------------------------------
    Rform = k * Rf
    R_viscous = Rf + Rform

    # --------------------------------------------------
    # Froude number
    # --------------------------------------------------
    Fn = V_ms / math.sqrt(g * L)

    # --------------------------------------------------
    # Wave-making resistance (FULL Holtrop–Mennen)
    # --------------------------------------------------
    Cm = 0.98
    Cp = CB / Cm
    iE = 10.0

    # c7 — Slenderness correction
    BL = B / L
    if BL < 0.11:
        c7 = 0.229577 * (BL ** 0.33333)
    elif 0.11 < BL < 0.25:
        c7 = BL
    else:
        c7 = 0.5 - 0.0625 * (L / B)

    # C1 — Main hull-form coefficient
    C1 = (
        2223105
        * (c7 ** 3.78613)
        * ((T / B) ** 1.07961)
        * ((90 - iE) ** -1.37565)
    )

    # c3 — Bulb influence
    A_BT = 0.01
    c3 = 0.56 * (A_BT ** 1.5) / (B * T * (0.31 * math.sqrt(A_BT) ))

    # C2 — Bulb correction factor
    C2 = math.exp(-1.89 * math.sqrt(c3))

    # C5 — Transom stern correction
    C5 = 1.0 - ((0.8 * A_BT) / (B*T*Cm))

    # C16 — Cp correction
    if Cp < 0.8:
        C16 = (
            8.07981 * Cp
            - 13.8673 * Cp**2
            + 6.984388 * Cp**3
        )
    else:
        C16 = 1.73014 - 0.7067 * Cp

    # m1 — Speed growth coefficient
    m1 = (
        0.0140407 * (L / T)
        - 1.75254 * (disp_volume ** (1/3) / L)
        - 4.79232 * (B / L)
        - C16
    )

    # m2 — Wave interference amplitude
    c15 = -1.69385
    m2 = c15 * Cp**2 * math.exp(-0.1 / (Fn**2))

    # λ — Wave phase parameter
    if (L / B) < 12:
        lam = 1.446 * Cp - 0.03 * (L / B)
    else:
        lam = 1.446 * Cp - 0.36

    # Exponent d
    d = -0.9

    # Final wave resistance
    if Fn < 0.20:
        Rw = 0.0
    else:
        Rw = (
            C1
            * C2
            * C5
            * rho
            * g
            * disp_volume
            * math.exp(m1 * (Fn ** d) + m2 * math.cos(lam / (Fn**2)))
        )

    # --------------------------------------------------
    # Bulbous bow resistance
    # --------------------------------------------------
    if Fn > 0.20:
        Rbulb = 0.11 * Rw
    else:
        Rbulb = 0.0

    # --------------------------------------------------
    # Total resistance
    # --------------------------------------------------
    RT = R_viscous + Rw + Rbulb
    
    

    # --------------------------------------------------
    # Power
    # --------------------------------------------------
    EHP = RT * V_ms
    DHP = EHP / eta_D
    # --------------------------------------------------
    # Total resistance coefficient (Ct)
    # --------------------------------------------------
    if V_ms > 0:
        Ct = RT / (0.5 * rho * V_ms**2 * S)
    else:
        Ct = 0.0

    # --------------------------------------------------
    # Return values (kN, kW)
    # --------------------------------------------------
    return (
     RT / 1000,
     EHP / 1000,
     DHP / 1000,
     Rf / 1000,
     Rform / 1000,
     Rw / 1000,
     C1,
     C2,
     C5,
     m1,
     m2,
     Rbulb / 1000,
     Ct

    )

