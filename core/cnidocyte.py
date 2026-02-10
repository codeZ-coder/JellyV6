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
        self.nematocisto_ativo = 0  # Cooldown counter (ciclos restantes)

    def avaliar_ameaca(self, is_anomaly: bool, down: float,
                       max_down_kbps: float, z_val: float) -> bool:
        """
        Avalia se deve ativar defesa e gerencia cooldown.
        Retorna True se reflexo está ativo.
        """
        if is_anomaly and self.nematocisto_ativo == 0:
            # Ativa defesa por 15 ciclos
            self.nematocisto_ativo = 15

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
            self.nematocisto_ativo = 15

        # Decrementa cooldown
        reflexo_ativo = self.nematocisto_ativo > 0
        if reflexo_ativo:
            self.nematocisto_ativo -= 1

        return reflexo_ativo

    def get_status_text(self, reflexo_ativo: bool, down: float,
                        max_down_kbps: float, z_val: float) -> str:
        """Retorna texto de status durante defesa ativa"""
        if not reflexo_ativo:
            return ""

        limite_atual = max_down_kbps * 0.8
        tipo = "SATURAÇÃO" if down > limite_atual else f"ANOMALIA Z:{z_val:.1f}"
        return f"⚠️ ALERTA: {tipo}"
