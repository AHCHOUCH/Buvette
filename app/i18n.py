from flask_login import current_user

TRANSLATIONS = {
    'fr': {
        'Dashboard':'Tableau de bord','Clients':'Clients','Users':'Utilisateurs','Suppliers':'Fournisseurs','Supplier Charges':'Charges fournisseurs','Charges':'Charges','Payments':'Paiements','Ledger':'Grand livre','Settings':'Paramètres','Logs':'Journaux','Breakfast':'Petit déjeuner','Lunch':'Déjeuner','Log out':'Déconnexion','Confirm':'Confirmer','Cancel':'Annuler','Amount':'Montant','Client':'Client','Password':'Mot de passe','Username':'Nom utilisateur','Login':'Connexion'},
    'ar': {
        'Dashboard':'لوحة التحكم','Clients':'الزبائن','Breakfast':'الفطور','Lunch':'الغداء','Payments':'الأداء','Ledger':'السجل','Log out':'تسجيل الخروج','Confirm':'تأكيد','Cancel':'إلغاء','Amount':'المبلغ','Client':'الزبون','Breakfast Order':'طلب الفطور','Lunch Charge':'وجبة الغداء','Cash Payment':'الأداء','Select client':'اختيار الزبون'}
}

def lang():
    try:
        return 'ar' if current_user.is_authenticated and current_user.role == 'cashier' else 'fr'
    except Exception:
        return 'fr'

def t(text):
    return TRANSLATIONS.get(lang(), {}).get(text, text)
