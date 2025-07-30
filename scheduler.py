import time
from datetime import datetime
from app import app, db
from app.models import Operation
from ib_utils import enviar_ordre_ib, get_exit_price_ib  # 👉 Dejamos los nombres de función como están

while True:
    now = datetime.now().time()
    print(f"⏰ Son las {datetime.now().strftime('%H:%M:%S')}... revisando operaciones...")

    with app.app_context():
        operations = Operation.query.all()

        for op in operations:
            # 🚀 Enviamos la orden si corresponde
            if op.entry_time <= now and not op.entry_price:
                resultat = enviar_ordre_ib(
                    symbol=op.symbol,
                    amount=op.amount,
                    direction=op.direction,
                    stop_loss_pct=op.stop_loss,
                    stop_profit_pct=op.stop_profit
                )

                if resultat["success"]:
                    op.entry_price = resultat["avgFillPrice"]
                    db.session.commit()
                    print(f"✅ Orden enviada para {op.symbol} a las {op.entry_time}")
                else:
                    print(f"❌ Error al enviar la orden para {op.symbol}: {resultat['error']}")

            # 🕰️ Registramos el precio de salida si corresponde
            if op.exit_time and now >= op.exit_time and not op.exit_price:
                resultat_exit = get_exit_price_ib(op.symbol)

                if resultat_exit["success"]:
                    op.exit_price = resultat_exit["exit_price"]
                    db.session.commit()
                    print(f"📉 Precio de salida registrado para {op.symbol}: {op.exit_price}")
                else:
                    print(f"⚠️ No se pudo obtener el precio de salida para {op.symbol}: {resultat_exit['error']}")

    time.sleep(60)  # 🔁 Esperamos un minuto antes de volver a comprobar
