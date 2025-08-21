from scraper import FootballDataScraper
import polars as pl
from scipy.stats import poisson






class liga():
    def __init__(self, url):
        self.url = url
        self.scraper = FootballDataScraper(url)

    def data(self):
        return self.scraper.scrape_data()
    
    def equipos_local(self):
        df = self.data()
        return df['Local'].unique().sort()       
        
    def equipos_visita(self):
        df = self.data()
        return df['Visita'].unique().sort()
        
    def promedioGFL(self):
        df = self.data()
        return df['GA'].mean()
         
    def promedioGCL(self):
        df = self.data()
        return df['GC'].mean()
        
    def promedioGFV(self):
        df = self.data()
        return df['GC'].mean()
        
    def promedioGCV(self):
        df = self.data()
        return df['GA'].mean()

        
    def promEFL(self,local):
        df = self.data()
        df = df.filter(pl.col("Local") == local)
        return df['GA'].mean()

        
    def promECL(self,local):
        df = self.data()
        df = df.filter(pl.col("Local") == local)
        return df['GC'].mean()

        
    def promEFV(self,visita):
        df = self.data()
        df = df.filter(pl.col("Visita") == visita)
        return df['GC'].mean()

    
    def promECV(self,visita):
        df = self.data()    
        df = df.filter(pl.col("Visita") == visita)
        return df['GA'].mean()

        
    def fuerzaOfensivaLocal(self, local):       
        return self.promEFL(local) / self.promedioGFL()
    
    def fuerzaDefensivaLocal(self, local):
        return self.promECL(local) / self.promedioGCL()
    
    def fuerzaOfensivaVisita(self, visita):
        return self.promEFV(visita) / self.promedioGFV()
    
    def fuerzaDefensivaVisita(self, visita):
        return self.promECV(visita) / self.promedioGCV()
        
    def fuerzaPromedioLocal(self, local, visita):
        return (self.fuerzaOfensivaLocal(local) * self.fuerzaDefensivaVisita(visita)) 
    
    def fuerzaPromedioVisita(self, local, visita):
        return (self.fuerzaOfensivaVisita(visita) * self.fuerzaDefensivaLocal(local)) 
    
    def EmpateResultado(self, local, visita):
        empate = 0.0
    
        fuerza_promedio_local = self.fuerzaPromedioLocal(local, visita)
        fuerza_promedio_visita = self.fuerzaPromedioVisita(local, visita)
    
        umbral = 1e-10
    
        for x in range(11):
        
            prob_local = poisson.pmf(x, fuerza_promedio_local)
            prob_visita = poisson.pmf(x, fuerza_promedio_visita)
            
           
            prob_empate_actual = prob_local * prob_visita
            empate += prob_empate_actual
         
            if prob_local < umbral or prob_visita < umbral:
                break
            
        return empate
            
                
            
    def VictoriaLocal(self, local, visita):
        victoria = 0.0
        fuerza_local = self.fuerzaPromedioLocal(local, visita)
        fuerza_visita = self.fuerzaPromedioVisita(local, visita)
        
        # Buclea solo los goles del equipo visitante (hasta un límite razonable)
        for y in range(21):
            prob_visita_y = poisson.pmf(y, fuerza_visita)
            
            # Probabilidad de que el local marque más de y goles
            prob_local_mas_y = 1 - poisson.cdf(y, fuerza_local)
            
            victoria += prob_visita_y * prob_local_mas_y
            
        return victoria
    
    def VictoriaVisita(self, local, visita):
        victoria = 0.0
        fuerza_local = self.fuerzaPromedioLocal(local, visita)
        fuerza_visita = self.fuerzaPromedioVisita(local, visita)
        
        # Buclea solo los goles del equipo local (hasta un límite razonable)
        for x in range(21):
            prob_local_x = poisson.pmf(x, fuerza_local)
            
            # Probabilidad de que el visitante marque más de x goles
            prob_visita_mas_x = 1 - poisson.cdf(x, fuerza_visita)
            
            victoria += prob_local_x * prob_visita_mas_x
            
        return victoria
        


    


        