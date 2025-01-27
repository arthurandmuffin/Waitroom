from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def check_patient_in(request):
    if request.method == 'POST':
        patient_id = request.POST.get('patientID')
        # Placeholder for future logic (e.g., database storage, validation)
        return render(request, 'check_patient_in.html', {'checked_in': True})
    return render(request, 'check_patient_in.html', {'checked_in': False})