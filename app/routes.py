import inspect
from ib_utils import enviar_ordre_ib
print("🔍 Fitxer que s'està usant per enviar_ordre_ib:", inspect.getfile(enviar_ordre_ib))


from flask import render_template, redirect, url_for, flash, request, Response
from app import app, db
from app.forms import OperationForm
from app.models import Operation
from datetime import datetime
import csv
from ib_utils import enviar_ordre_ib
import asyncio

@app.route("/add", methods=["GET", "POST"])
def add_operation():
    form = OperationForm()
    if form.validate_on_submit():
        try:
            entry_time = datetime.strptime(form.entry_time.data, "%H:%M:%S").time()
            exit_time = datetime.strptime(form.exit_time.data, "%H:%M:%S").time()
        except ValueError:
            flash("Formato de hora incorrecto. Usa HH:MM:SS", "error")
            return render_template('add.html', form=form)

        broker = form.broker.data

        op = Operation(
            symbol=form.symbol.data,
            amount=form.amount.data,
            entry_time=entry_time,
            exit_time=exit_time,
            stop_loss=form.stop_loss.data,
            stop_profit=form.stop_profit.data,
            direction=form.direction.data,
            broker=broker
        )
        db.session.add(op)
        db.session.commit()
        flash("Operación añadida correctamente", "success")
        return redirect(url_for('operations'))

    return render_template('add.html', form=form)


@app.route('/operations')
def operations():
    today = datetime.now().date()
    operations_today = Operation.query.filter(db.func.date(Operation.created_at) == today).all()
    all_operations = Operation.query.all()
    return render_template('operations.html', operations_today=operations_today, operations_all=all_operations)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/delete/<int:operation_id>', methods=["POST"])
def delete_operation(operation_id):
    op = Operation.query.get_or_404(operation_id)
    db.session.delete(op)
    db.session.commit()
    flash("🗑️ Operación eliminada!", "success")
    return redirect(url_for('operations'))

@app.route('/export')
def export_csv():
    operations = Operation.query.all()

    def generate():
        data = [
            ['ID', 'Símbolo', 'Importe', 'Entrada', 'Sortida', 'Stop Loss', 'Stop Profit', 'Dirección', 'Broker', 'Creado en']
        ]
        for op in operations:
            data.append([
                op.id,
                op.symbol,
                op.amount,
                op.entry_time.strftime('%H:%M:%S'),
                op.exit_time.strftime('%H:%M:%S'),
                op.stop_loss,
                op.stop_profit,
                op.direction,
                op.broker,
                op.created_at.strftime('%d/%m/%Y %H:%M:%S')
            ])

        output = []
        for row in data:
            output.append(','.join([str(cell) for cell in row]))
        return '\n'.join(output)

    return Response(
        generate(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment;filename=operacions.csv'}
    )

@app.route('/export-today')
def export_csv_today():
    today = datetime.now().date()
    operations = Operation.query.filter(db.func.date(Operation.created_at) == today).all()

    def generate():
        data = [
            ['ID', 'Símbolo', 'Importe', 'Entrada', 'Sortida', 'Stop Loss', 'Stop Profit', 'Dirección', 'Broker', 'Creado en']
        ]
        for op in operations:
            data.append([
                op.id,
                op.symbol,
                op.amount,
                op.entry_time.strftime('%H:%M:%S'),
                op.exit_time.strftime('%H:%M:%S'),
                op.stop_loss,
                op.stop_profit,
                op.direction,
                op.broker,
                op.created_at.strftime('%d/%m/%Y %H:%M:%S')
            ])

        output = []
        for row in data:
            output.append(','.join([str(cell) for cell in row]))
        return '\n'.join(output)

    return Response(
        generate(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment;filename=operacions_avui.csv'}
    )

@app.route('/simular')
def simular_operacions():
    from app.models import Operation
    from datetime import datetime, time
    import random

    for i in range(1):
        entry_price = round(random.uniform(120, 160), 2)
        exit_price = round(entry_price + random.uniform(-10, 10), 2)

        op = Operation(
            symbol="TSLA",
            amount=random.randint(1, 10),
            entry_time=time(10, 0),
            exit_time=time(15, 30),
            entry_price=entry_price,  # Nou camp
            exit_price=exit_price,    # Ara relacionat amb entry_price
            stop_loss=5.0,
            stop_profit=15.0,
            direction="long",
            broker="Interactive Brokers",
            created_at=datetime.now()
        )
        db.session.add(op)

    db.session.commit()
    return "Simulació completada ✅"

@app.route('/enviar_ib/<int:operation_id>')
def send_to_ib(operation_id):
    op = Operation.query.get_or_404(operation_id)

    resultat = enviar_ordre_ib(
        op.symbol,
        op.amount,
        op.direction,
        op.stop_loss,
        op.stop_profit if op.stop_profit else None
    )

    if resultat["success"]:
        op.entry_price = resultat["avgFillPrice"]
        db.session.commit()
        flash(f"✅ Operació enviada a IB amb èxit. Ordre ID: {resultat['status']}", "success")
    else:
        flash(f"❌ Error en enviar operació: {resultat['error']}", "danger")

    return redirect(url_for('operations'))
