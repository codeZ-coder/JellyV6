"""
🪼 Jelly V6 - Cnidocyte Module (Defesa)
Gerencia o disparo de nematocistos, cooldown e forense.
Nome: Cnidocyte = célula de defesa das águas-vivas reais (contém o nematocisto).
"""
import logging

logger = logging.getLogger(__name__)


class Cnidocyte:
    """Arsenal defensivo da Jelly — cooldown + disparo forense"""

    def __init__(self, persistence):
        """
        Args:
            persistence: instância de Persistence para registro forense
        """
        self.persistence = persistence
        self.nematocisto_ativo = 0  # Dwell Time Ativo (Contador de Defesa)
        self.refractory_timer = 0   # Dwell Time Passivo (Periodo Refratario)

    def avaliar_ameaca(self, is_anomaly: bool, down: float,
                       max_down_kbps: float, z_val: float,
                       osmotic_alert: str = None) -> bool:
        """
        Avalia se deve ativar defesa e gerencia cooldown.
        Retorna True se reflexo está ativo.
        
        Args:
            osmotic_alert: Ação da membrana osmótica (NEMATOCYST, RUPTURA_MESOGLEIA, etc.)
        """
        # Conexão Mente-Corpo: alerta osmótico ativa defesa imediatamente
        if osmotic_alert in ("NEMATOCYST", "RUPTURA_MESOGLEIA"):
            self.nematocisto_ativo = 15
            self.refractory_timer = 0  # Defesa crítica ignora tempo de calma
            self.persistence.registrar_forense_async(
                "ALERTA_OSMOTICO",
                f"Tipo: {osmotic_alert} | Flow: {down:.0f}"
            )

        elif is_anomaly and self.nematocisto_ativo == 0:
            # DWELL TIME (Histerese): Se está em período refratário, ignora anomalias leves
            if self.refractory_timer > 0:
                logger.debug(f"HISTERESE: Ignorando anomalia durante periodo refratario ({self.refractory_timer}s)")
                self.refractory_timer -= 1
                return False

            # Ativa defesa por 15 ciclos (Dwell Time Ativo)
            self.nematocisto_ativo = 15
            self.refractory_timer = 0

            # Determina tipo de ameaça e dispara forense em background
            limite_atual = max_down_kbps * 0.8
            if down > limite_atual:
                self.persistence.registrar_forense_async(
                    "SATURACAO_REDE",
                    f"Flow: {down:.0f} > Lim: {limite_atual:.0f}"
                )
            else:
                self.persistence.registrar_forense_async(
                    "ANOMALIA_Z_SCORE",
                    f"Z: {z_val:.2f} (Flow: {down:.0f})"
                )

        elif is_anomaly and self.nematocisto_ativo > 0:
            # Já em defesa — apenas renova o cooldown
            # Dwell Time Ativo: Garante que fique em defesa por mais tempo
            self.nematocisto_ativo = 15
        
        # Decrementa cooldown de ATIVIDADE
        if self.nematocisto_ativo > 0:
            self.nematocisto_ativo -= 1
            # Se acabou a defesa, inicia periodo refratario (Calm Dwell Time)
            if self.nematocisto_ativo == 0:
                self.refractory_timer = 10  # 10 ciclos de paz obrigatÃ³ria

        reflexo_ativo = self.nematocisto_ativo > 0
        return reflexo_ativo


    def get_status_text(self, reflexo_ativo: bool, down: float,
                        max_down_kbps: float, z_val: float) -> str:
        """Retorna texto de status durante defesa ativa"""
        if not reflexo_ativo:
            return ""

        limite_atual = max_down_kbps * 0.8
        tipo = "SATURAÇÃO" if down > limite_atual else f"ANOMALIA Z:{z_val:.1f}"
        return f"⚠️ ALERTA: {tipo}"
