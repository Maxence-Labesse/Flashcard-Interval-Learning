from import_files import fichier_boite


def avancer_boite(df, q_id):
    df_tmp = df.copy()
    id_boite = df_tmp.loc[df["ID"] == q_id, "boite"].values[0]

    if id_boite < 4:
        df_tmp.loc[df["ID"] == q_id, "boite"] += 1

    return df_tmp


def reculer_boite(df, q_id):
    df_tmp = df.copy()
    id_boite = df_tmp.loc[df["ID"] == q_id, "boite"].values[0]

    if id_boite > 0:
        df_tmp.loc[df["ID"] == q_id, "boite"] -= 1

    return df_tmp


def save_boite(df_boite):
    df_boite.to_csv(fichier_boite, index=False)
