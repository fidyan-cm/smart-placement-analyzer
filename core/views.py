import os
import json
import joblib
import numpy as np
from datetime import datetime

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string

from .forms import StudentForm
from .models import Student
from .hackerrank import get_hackerrank_profile
from .skill_gap import compute_skill_gap

# ── Load model bundle once at startup ────────────────────────
MODEL_PATH   = os.path.join(settings.BASE_DIR, 'placement_model.pkl')
bundle       = joblib.load(MODEL_PATH)
model        = bundle['model']
scaler       = bundle['scaler']
uses_scaling = bundle['uses_scaling']


@login_required
def predict_placement(request):
    form   = StudentForm()
    result = None

    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            # ── HackerRank scrape (optional) ──────────────────
            hr_username = data.get('hackerrank_username', '').strip()
            hr_profile  = None
            if hr_username:
                hr_profile = get_hackerrank_profile(hr_username)
                if not hr_profile.get('error'):
                    data['hackerrank_score'] = hr_profile['technical_score']

            # ── ML Prediction ─────────────────────────────────
            features = np.array([[
                data['cgpa'],
                data['internships'],
                data['projects'],
                data['technical_skills_score'],
                data['hackerrank_score'],
            ]])

            if uses_scaling:
                features = scaler.transform(features)

            prediction  = model.predict(features)[0]
            probability = model.predict_proba(features)[0][1]

            if prediction == 1:
                status = 'High Probability of Placement'
                badge  = 'success'
            else:
                status = 'Skill Enhancement Required'
                badge  = 'danger'

            # ── Skill Gap Analysis ────────────────────────────
            gap_report = compute_skill_gap({
                'cgpa':                   data['cgpa'],
                'internships':            data['internships'],
                'projects':               data['projects'],
                'technical_skills_score': data['technical_skills_score'],
                'hackerrank_score':       data['hackerrank_score'],
            })

            # ── Save to DB ────────────────────────────────────
            Student.objects.create(
                name=data['name'],
                cgpa=data['cgpa'],
                internships=data['internships'],
                projects=data['projects'],
                technical_skills_score=data['technical_skills_score'],
                hackerrank_score=data['hackerrank_score'],
                placement_status=status,
                prediction_probability=round(float(probability), 4),
            )

            result = {
                'name':            data['name'],
                'status':          status,
                'badge':           badge,
                'probability':     round(probability * 100, 2),
                'gap_report':      gap_report,
                'hr_profile':      hr_profile,
                'radar_labels':    json.dumps(gap_report['radar_labels']),
                'radar_student':   json.dumps(gap_report['radar_student']),
                'radar_benchmark': json.dumps(gap_report['radar_benchmark']),
            }

    return render(request, 'core/predict.html', {
        'form':   form,
        'result': result,
    })


@login_required
def history(request):
    students = Student.objects.all()
    return render(request, 'core/history.html', {'students': students})


@login_required
def download_report(request):
    if request.method != 'POST':
        return redirect('predict')

    data = {
        'name':                   request.POST.get('name'),
        'cgpa':                   float(request.POST.get('cgpa', 0)),
        'internships':            int(request.POST.get('internships', 0)),
        'projects':               int(request.POST.get('projects', 0)),
        'technical_skills_score': int(request.POST.get('technical_skills_score', 0)),
        'hackerrank_score':       int(request.POST.get('hackerrank_score', 0)),
        'probability':            float(request.POST.get('probability', 0)),
        'status':                 request.POST.get('status'),
        'badge':                  request.POST.get('badge'),
    }

    gap_report = compute_skill_gap({
        'cgpa':                   data['cgpa'],
        'internships':            data['internships'],
        'projects':               data['projects'],
        'technical_skills_score': data['technical_skills_score'],
        'hackerrank_score':       data['hackerrank_score'],
    })

    result = {
        'name':        data['name'],
        'status':      data['status'],
        'badge':       data['badge'],
        'probability': data['probability'],
        'gap_report':  gap_report,
    }

    html_string = render_to_string('core/report_pdf.html', {
        'result':       result,
        'generated_on': datetime.now().strftime('%d %B %Y, %I:%M %p'),
    })

    try:
        from xhtml2pdf import pisa
        from io import BytesIO

        buffer   = BytesIO()
        pisa_status = pisa.CreatePDF(html_string, dest=buffer)

        if pisa_status.err:
            return HttpResponse('PDF generation failed.', status=500)

        buffer.seek(0)
        filename = f"placement_report_{data['name'].replace(' ', '_')}.pdf"
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response

    except Exception as e:
        return HttpResponse(f"PDF generation failed: {str(e)}", status=500)