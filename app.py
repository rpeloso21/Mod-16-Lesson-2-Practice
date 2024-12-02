from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

app = Flask(__name__)
ma = Marshmallow(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://example_sum_postgres_mtk8_user:XagGn67OROsXKqFqeTgJtPgeawzy0hBE@dpg-ct6pra1u0jms739b2mag-a.oregon-postgres.render.com/example_sum_postgres_mtk8'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(app, model_class=Base)

class Sum(Base):
    __tablename__ = "Sum"
    id: Mapped[int] = mapped_column(primary_key = True)
    num1: Mapped[int] = mapped_column(db.Integer, nullable=False)
    num2: Mapped[int] = mapped_column(db.Integer, nullable=False)
    result: Mapped[int] = mapped_column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Sum {self.id}: {self.num1} + {self.num2} = {self.result}>"
    

class SumSchema(ma.Schema):
    id = fields.Integer()
    nym1 = fields.Integer()
    nym2 = fields.Integer()
    result = fields.Integer()

sums_schema = SumSchema(many=True)

@app.route("/sum", methods=['GET'])
def find_all():
    sums = db.session.execute(db.select(Sum)).scalars()
    return sums_schema.jsonify(sums), 200



@app.route("/sum", methods=['POST'])
def sum():
    data = request.get_json()
    num1 = data['num1']
    num2 = data['num2']
    result = num1 + num2

    with Session(db.engine) as session:
        with session.begin():
            sum_entry = Sum(num1=num1, num2=num2, result=result)
            session.add(sum_entry)

    return jsonify({'result': result})

@app.route("sum/result/<int:result>", methods=['POST'])
def find_by_result(result):
    sums = db.session.execute(db.select(Sum).where(Sum.result == result)).scalars()
    return sums_schema.jsonify(sums), 200


with app.app_context():
    db.drop_all()
    db.create_all()
# if __name__ == '__main__':
#     app.run(debug=True)