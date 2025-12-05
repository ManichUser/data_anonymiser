import pandas as pd

# Données patients
patients = pd.DataFrame({
    'patient_id': ['P001', 'P002', 'P003', 'P004', 'P005'],
    'nom': ['Dupont', 'Kamga', 'Ngo', 'Mbarga', 'Fotso'],
    'prenom': ['Marie', 'Jean', 'Sophie', 'Paul', 'Claire'],
    'email': ['marie.d@email.com', 'jean.k@email.com', 'sophie.n@email.com', 
              'paul.m@email.com', 'claire.f@email.com'],
    'telephone': ['+237670123456', '+237670234567', '+237670345678', 
                  '+237670456789', '+237670567890'],
    'date_naissance': ['1985-03-15', '1990-07-22', '1978-11-30', 
                       '1995-01-10', '1988-09-05'],
    'ville': ['Yaoundé', 'Douala', 'Bafoussam', 'Yaoundé', 'Douala']
})

# Données consultations
consultations = pd.DataFrame({
    'patient_id': ['P001', 'P002', 'P003', 'P001', 'P004', 'P005', 'P002'],
    'date_consultation': ['2024-01-15', '2024-01-20', '2024-02-10', 
                         '2024-02-15', '2024-03-01', '2024-03-10', '2024-03-15'],
    'medecin': ['Dr. Ateba', 'Dr. Nguema', 'Dr. Ateba', 'Dr. Nguema', 
                'Dr. Ateba', 'Dr. Nguema', 'Dr. Ateba'],
    'diagnostic': ['Grippe', 'Hypertension', 'Diabète', 'Contrôle', 
                   'Migraine', 'Gastrite', 'Contrôle'],
    'cout_fcfa': [15000, 25000, 30000, 10000, 12000, 18000, 10000]
})

# Sauvegarder
patients.to_excel('mock/patients.xlsx', index=False)
consultations.to_excel('mock/consultations.xlsx', index=False)
print("✅ Fichiers créés avec succès !")