# -*- coding: utf-8 -*-
# quiz-orm/views.py

from flask import Flask
from flask import render_template, request, redirect, url_for, abort, flash
from modele import *
from forms import *

app = Flask(__name__)

@app.route('/')
def index():
    """Strona główna"""
    return render_template('index.html')

@app.route('/lista_uczniow')
def lista_ucz():
    uczniowie = Uczen.select()
    return render_template('lista_uczniow.html', query=uczniowie)
    
@app.route('/lista_klas')
def lista_kl():
    klasy = Klasa.select()
    return render_template('lista_klas.html', query=klasy)
    
    
@app.route('/dodaj_klasa', methods=['GET', 'POST'])
def dodaj_kl():
    form = DodajForm()
    form.klasa.choices = [(k.id, k.klasa) for k in Klasa.select()]
    
    if form.validate_on_submit():
        print(form.data)
        k = Klasa(klasa=form.klasa.data, rok_naboru=form.rok_naboru.data, rok_matury=form.rok_matury.data)
        k.save()
        
        flash("Dodano klasę!", "sukces")
        return redirect(url_for('index'))
    elif request.method == 'POST':
        flash_errors(form)
        
    return render_template('dodaj_klasa.html', form=form)

@app.route('/dodaj_ucznia', methods=['GET', 'POST'])
def dodaj_ucz():
    form = DodajUczForm()
    form.klasa.choices = [(k.id, k.klasa) for k in Klasa.select()]

    if form.validate_on_submit():
        print(form.data)
        k = Uczen(imie=form.imie.data, nazwisko=form.nazwisko.data,
                  plec=form.plec.data, klasa=form.klasa.data)
        k.save()
        flash("Dodano ucznia!", "sukces")
        return redirect(url_for('index'))
    elif request.method == 'POST':
        flash_errors(form)

    return render_template('dodaj_ucznia.html', form=form)

def get_or_404(obiekt, id):
    try:
        o = obiekt.get_by_id(id)
        return o
    except Klasa.DoesNotExist:
        abort(404)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/klasa_usun/<int:kid>', methods=['GET', 'POST'])
def klasa_usun(kid):
    """Usuwanie klasy o podanym id"""
    k = get_or_404(Klasa, kid)
    if request.method == 'POST':
        flash('Usunięto klase {}'.format(k.klasa), 'sukces')
        k.delete_instance()
        return redirect(url_for('index'))
    return render_template('klasa_usun.html', klasa=k)


@app.route('/klasa_edytuj/<int:kid>', methods=['GET', 'POST'])
def klasa_edytuj(kid):
    """Edycja pytan i odpowiedzi"""
    k = get_or_404(Klasa, kid)

    form = DodajForm(obj=k)

    if form.validate_on_submit():
        k.klasa = form.klasa.data
        k.rok_matury = form.rok_matury.data
        k.rok_naboru = form.rok_naboru.data
        k.save()
        flash("Zaktualizowano klasę: {}".format(form.klasa.data))
        redirect(url_for('lista_klas'))
    else:
        flash_errors(form)

    return render_template('klasa_edytuj.html', form=form)

@app.route('/uczen_edytuj/<int:kid>', methods=['GET', 'POST'])
def uczen_edytuj(kid):
  
    k = get_or_404(Uczen, kid)

    form = DodajUczForm(obj=k)

    if form.validate_on_submit():
        k.imie = form.imie.data
        k.nazwisko = form.nazwisko.data
        k.plec = form.plec.data
        k.klasa = form.klasa.data
        k.save()
        flash("Zaktualizowano ucznia: {}".format(form.imie.data))
        redirect(url_for('lista_uczniow'))
    else:
        flash_errors(form)

    return render_template('uczen_edytuj.html', form=form)
