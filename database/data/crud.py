from database.connection import Connection
from models.response_model import Response
from datetime import datetime, date
import calendar

class Crud:
    def __init__(self):
        self.connection = Connection()
        
    def sales_today(self):
        try:
            with self.connection.conn() as conn:
                with conn.cursor() as cur:
                    today = date.today()
                                        
                    query = "SELECT SUM(total) AS total_sales FROM public.sales WHERE sale_date::date = %s"
                    cur.execute(query, (today,))
                    response = cur.fetchone()
                    
                    if response[0] is None:
                        return Response(success=False, error="No se encontraron ventas para hoy")
                    else:
                        total_sales_per_today = response[0]
                        
                        return Response(success=True, data=total_sales_per_today)
        except Exception as e:
            return Response(success=False, error=str(e))
    
    def sales_by_date(self, target_date: str):
        try:
            with self.connection.conn() as conn:
                with conn.cursor() as cur:
                    
                    target_date = datetime.strptime(target_date, '%Y-%m-%d').date()
                    
                    query = "SELECT SUM(total) AS total_sales FROM public.sales WHERE sale_date::date = %s"
                    cur.execute(query, (target_date,))
                    response = cur.fetchone()
                    
                    if response[0] is None:
                        return Response(success=False, error=f"No se encontraron ventas para la fecha {target_date}")
                    else:
                        total_sales_per_date = response[0]
                        
                        return Response(success=True, data=total_sales_per_date)
        except Exception as e:
            return Response(success=False, error=str(e))
    
    def sales_by_month(self):
        try:
            with self.connection.conn() as conn:
                with conn.cursor() as cur:
                    
                    today = date.today()
                    year = today.year
                    month = today.month

                        
                    first_day_of_month = datetime(year, month, 1).date()
                    last_day_of_month = datetime(year, month, calendar.monthrange(year, month)[1]).date()
                    
                    
                    query = "SELECT SUM(total) AS total_sales FROM public.sales WHERE sale_date::date BETWEEN %s AND %s"
                    cur.execute(query, (first_day_of_month, last_day_of_month))
                    response = cur.fetchone()
                    
                    if response[0] is None:
                        return Response(success=False, error=f"No se encontraron ventas entre {first_day_of_month} y {last_day_of_month}")
                    else:
                        total_sales_per_range = response[0]
                        
                        return Response(success=True, data=total_sales_per_range)
        except Exception as e:
                return Response(success=False, error=str(e))
    
    def top_10_best_selling_products(self):
        try:
            with self.connection.conn() as conn:
                with conn.cursor() as cur:
                    
                    query = """
                    SELECT sp.product_id,
                           p.name,
                           p.reference,
                           COUNT(*) AS total_repeticiones
                    FROM public.sale_products sp
                    JOIN public.products p ON sp.product_id = p.id
                    GROUP BY sp.product_id, p.name, p.reference
                    ORDER BY total_repeticiones DESC
                    LIMIT 10;
                    """
                    
                    cur.execute(query)
                    response = cur.fetchall()
                    
                    if not response:
                        return Response(success=False, error="No se encontraron productos vendidos")
                    else:
                        # Convertir los resultados a una lista de diccionarios
                        top_products = []
                        for product in response:
                            product_data = {
                                "product_id": product[0],
                                "name": product[1],
                                "reference": product[2],
                                "total_sold": product[3]
                            }
                            top_products.append(product_data)
                        
                        return Response(success=True, data=top_products)
        except Exception as e:
            return Response(success=False, error=str(e))