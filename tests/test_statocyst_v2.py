from core.statocyst import Statocyst, LIMIT_CPU_PANIC
import statistics

def test_statocyst_normal_traffic():
    """Trafego estavel nao deve gerar anomalia."""
    st = Statocyst()
    # Encher baseline com 1000kbps (variando pouco)
    for _ in range(50):
        st.analyze_network(1000.0)
    
    # Trafego atual tambem 1000
    is_anomaly, z_val, _ = st.analyze_network(1005.0)
    
    assert not is_anomaly
    assert z_val < 3.0

def test_statocyst_spike_anomaly():
    """Pico repentino deve ser detectado (Short vs Long)."""
    st = Statocyst()
    # Baseline normal (100)
    for _ in range(50):
        st.analyze_network(100.0)
    
    # Injetar pico (500) que eh > 3 desvios padrao
    # Se stdev for 50 (minimo), mean=100.
    # (500 - 100) / 50 = 8.0 -> Anomaly!
    
    is_anomaly, z_val, _ = st.analyze_network(600.0)
    
    assert is_anomaly
    assert z_val > 3.0

def test_statocyst_panic_limit():
    """Deve detectar limite absoluto (80% do maximo)."""
    st = Statocyst(max_down_kbps=1000.0)
    
    # 900 > 800 (80%)
    is_anomaly, z_val, updated = st.analyze_network(900.0)
    
    assert is_anomaly
    assert z_val == 100.0
    assert not updated # Nao eh maior que 1000

def test_statocyst_learning():
    """Deve aprender novo maximo."""
    st = Statocyst(max_down_kbps=1000.0)
    
    is_anomaly, z_val, updated = st.analyze_network(1200.0)
    
    assert updated
    assert st.max_down_kbps == 1200.0
