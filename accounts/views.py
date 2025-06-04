from django.shortcuts import render, redirect
from .forms import RegistrationForm

def register(request):
    try:
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('register')
        else:
            form = RegistrationForm()
        return render(request, 'accounts/register.html', {'form': form})
    except Exception as e:
        return render(request, 'accounts/error.html', {'error': str(e)})
