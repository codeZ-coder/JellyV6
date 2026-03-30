import time
import random
from typing import Dict, List, Optional

class OsmoticMembrane:
    """
    Simula uma membrana semipermeável com recuperação elástica e discriminação de ameaças.
    
    Novos Conceitos:
    - Recuperação Osmótica: Pressão cai com o tempo (homeostase).
    - Discriminação Orgânica: Diferencia erro humano de ataque bot.
    """
    
    def __init__(self, threshold_atm: int = 150, decay_rate: int = 5):
        self.pressure_atm = 0       
        self.threshold = threshold_atm 
        self.decay_rate = decay_rate # Recuperação por ciclo
        self.is_ruptured = False    
        self.last_update = time.time()

    def osmotic_recovery(self):
        """Simula a homeostase (recuperação natural da célula)."""
        now = time.time()
        # Se passou tempo suficiente, reduz a pressão
        if now - self.last_update > 1.0: 
            if self.pressure_atm > 0:
                self.pressure_atm = max(0, self.pressure_atm - self.decay_rate)
                print(f"[HOMEOSTASE] Recuperando... Pressão caiu para {self.pressure_atm} atm")
            self.last_update = now

    def sense_ion(self, ion_type: str, ion_charge: int, is_organic: bool = False):
        """
        Detecta evento com discriminação de origem (Humano vs Bot).
        """
        if self.is_ruptured: return 

        # Fator de amplificação para Bots (x2 carga)
        final_charge = ion_charge if is_organic else ion_charge * 2
        origin = "ORGÂNICO" if is_organic else "INORGÂNICO (BOT)"
        
        print(f"[SENSOR] Íon: {ion_type} | Origem: {origin} | Carga: +{final_charge} atm")
        
        self.pressure_atm += final_charge
        self._check_pressure(is_organic)

    def _check_pressure(self, is_organic: bool):
        print(f"[MEMBRANA] Pressão Interna: {self.pressure_atm}/{self.threshold} atm")
        
        if self.pressure_atm >= self.threshold:
            if is_organic:
                self._contract_muscle() # Apenas bloqueio temporário
            else:
                self._fire_nematocyst() # Disparo letal

    def _contract_muscle(self):
        """Resposta não-letonal para orgânicos (Bloqueio Temporário)."""
        print("\n" + "#"*40)
        print("⚠️  SOBRECARGA ORGÂNICA DETECTADA ⚠️")
        print(">>> Iniciando Contração Muscular (Rate Limit/Captcha) <<<")
        print("#"*40 + "\n")
        # Reduz pressão pela metade para dar chance
        self.pressure_atm = int(self.pressure_atm / 2) 

    def _fire_nematocyst(self):
        self.is_ruptured = True
        print("\n" + "!"*40)
        print("⚡ RUPTURA DE MEMBRANA (INORGÂNICA) ⚡")
        print("!!! DISPARANDO NEMATOCISTO + PORINAS !!!")
        print("!"*40 + "\n")
        self._release_neurotoxins()
        self._open_porins()

    def _release_neurotoxins(self):
        print("[TOXINA] Injetando Neurotoxinas... (Blackhole Route)")

    def _open_porins(self):
        print("[PORINAS] Injetando GZIP BOMB no fluxo de resposta...")

# --- Simulação Avançada ---
def advanced_simulation():
    cell = OsmoticMembrane(threshold_atm=100, decay_rate=10)
    
    actions = [
        # (Ação, Carga, É Humano?)
        ("Erro de Senha (User)", 15, True),
        ("Erro de Senha (User)", 15, True),
        ("Erro de Senha (User)", 15, True),
        ("WAIT", 0, False), # Tempo para recuperação
        ("WAIT", 0, False),
        ("Scanner Bot (SQLi)", 40, False), # Bot = Carga x2 (80 atm)
        ("Scanner Bot (XSS)", 30, False)   # Bot = Carga x2 (60 atm) -> ESTRONDO!
    ]

    print("--- SIMULAÇÃO AVANÇADA (Homeostase + Discriminação) ---\n")
    
    for action, charge, is_organic in actions:
        if cell.is_ruptured: break
        
        time.sleep(1.2) # Tempo para homeostase agir
        cell.osmotic_recovery()
        
        if action == "WAIT":
            print("... (Tempo passando) ...")
            continue
            
        print(f"\nAtividade: {action}")
        cell.sense_ion("Event", charge, is_organic)
        print("-" * 30)

if __name__ == "__main__":
    advanced_simulation()
