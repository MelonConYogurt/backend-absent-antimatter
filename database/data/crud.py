from database.connection import Connection
from models.response_model import Response, Metadata
from datetime import datetime, date

class Crud:
    def __init__(self):
        self.connection = Connection()
        
    def sales_today(self):
        try:
            with self.connection.conn() as conn:
                with conn.cursor() as cur:
                    today = date.today()
                                        
                    query = "SELECT * FROM public.sales WHERE DATE(sale_date) = %s"
                    cur.execute(query, (today,))
                    response = cur.fetchall()
                    
                    if not response:
                        return Response(success=False, error="No se encontraron ventas para hoy")
                    else:
                        total_sales_per_today = 0
                        for sale in response:
                            total_sales_per_today += int(sale[4])
                        
                        return Response(success=True, data=total_sales_per_today)
        except Exception as e:
            return Response(success=False, error=str(e))
    
    def sales_by_date(self, target_date: str):
        try:
            with self.connection.conn() as conn:
                with conn.cursor() as cur:
                    
                    target_date = datetime.strptime(target_date, '%Y-%m-%d')
                    
                    query = "SELECT * FROM public.sales WHERE DATE(sale_date) = %s"
                    cur.execute(query, (target_date,))
                    response = cur.fetchall()
                    
                    if not response:
                        return Response(success=False, error=f"No se encontraron ventas para la fecha {target_date}")
                    else:
                        total_sales_per_date = 0
                        for sale in response:
                            total_sales_per_date += int(sale[4])
                        
                        return Response(success=True, data=total_sales_per_date)
        except Exception as e:
            return Response(success=False, error=str(e))
    
    def sales_by_date_range(self, start_date: str, end_date: str):
  
        try:
            with self.connection.conn() as conn:
                with conn.cursor() as cur:
                    start_date = datetime.strptime(start_date, '%Y-%m-%d')
                    end_date = datetime.strptime(end_date, '%Y-%m-%d')
                    
                    query = "SELECT * FROM public.sales WHERE DATE(sale_date) BETWEEN %s AND %s"
                    cur.execute(query, (start_date, end_date))
                    response = cur.fetchall()
                    
                    if not response:
                        return Response(success=False, error=f"No se encontraron ventas entre {start_date} y {end_date}")
                    else:
                        total_sales_per_range = 0
                        for sale in response:
                            total_sales_per_range += int(sale[4])
                        
                        return Response(success=True, data=total_sales_per_range)
        except Exception as e:
            return Response(success=False, error=str(e))