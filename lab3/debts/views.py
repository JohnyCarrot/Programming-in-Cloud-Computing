import io
import zipfile
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from debts.forms import DebtorForm
from debts.models import Debtor


def add_form_errors_to_messages(request, form):
    for field, errors in form.errors.items():
        for error in errors:
            if field == '__all__':
                messages.warning(request, f'{error}')
            else:
                messages.warning(request, f'{form.fields[field].label}: {error}')

def index(request):
    all_depts = Debtor.objects.all()
    for dept in all_depts:
        dept.form = DebtorForm(instance=dept)
    context = {
        'all_depts': all_depts,
        "create_form": DebtorForm(),
    }
    return render(request,'index.html',context)

def debtor_create(request):
    if request.method != "POST":
        return redirect("index")

    form = DebtorForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Debt created.")
    else:
        add_form_errors_to_messages(request, form)
    return redirect("index")

def debtor_update(request, pk):
    debtor = get_object_or_404(Debtor, pk=pk)
    if request.method != "POST":
        return redirect("index")

    form = DebtorForm(request.POST, instance=debtor)
    if form.is_valid():
        form.save()
        messages.success(request, "Debt updated.")
    else:
        add_form_errors_to_messages(request, form)
    return redirect("index")

def debtor_delete(request, pk):
    debtor = get_object_or_404(Debtor, pk=pk)
    if request.method == "POST":
        name = debtor.name
        debtor.delete()
        messages.info(request, f'Debt of "{name}" deleted.')
    return redirect("index")

def debtor_toggle_paid(request, pk):
    debtor = get_object_or_404(Debtor, pk=pk)
    if request.method == "POST":
        debtor.is_paid = not debtor.is_paid
        debtor.save()
        messages.success(request, f'Dept of {debtor.name} marked as {"paid" if debtor.is_paid else "unpaid"}.')
    return redirect("index")

def run_migrations(request):
    from django.http import HttpResponse
    from django.core.management import call_command
    call_command("migrate", interactive=False)
    return HttpResponse("Migrácie boli spustené.")

import os
from django.conf import settings
from django.http import HttpResponse

def download_data(request):
    base_dir = settings.BASE_DIR
    buffer = io.BytesIO()

    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(base_dir):
            dirs[:] = [d for d in dirs if not d.startswith(".")]

            for file in files:
                if file.startswith("."):
                    continue

                full = os.path.join(root, file)
                relative = os.path.relpath(full, base_dir)
                zipf.write(full, relative)

    buffer.seek(0)

    response = HttpResponse(buffer.getvalue(), content_type="application/zip")
    response["Content-Disposition"] = 'attachment; filename="projekt.zip"'
    return response
