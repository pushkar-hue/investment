from simulation.engine.simulation_engine import MarketSimulation
from analysis.visualization.consensus_viz import visualize_streamlet
from datetime import datetime, timedelta

def run_consensus_simulation():
    sim = MarketSimulation(
        start_time=datetime.utcnow(),
        end_time=datetime.utcnow() + timedelta(minutes=5),
        time_step=timedelta(milliseconds=100)
    )
    
    # Setup market as before...
    
    results = sim.run()
    visualize_streamlet(results["consensus_data"])
    print("Consensus visualization saved as streamlet_blockchain.png")

if __name__ == "__main__":
    run_consensus_simulation()