from dataclasses import dataclass, field
from typing import List, Dict, Set, Optional
import hashlib
import random

@dataclass
class Block:
    epoch: int
    parent_hash: str
    transactions: List[str]  # Simplified for demo
    hash: str = None
    notarized: bool = False
    finalized: bool = False
    proposer: int = None
    voters: Set[int] = field(default_factory=set)  # FIXED: Use default_factory

    def __post_init__(self):
        if not self.hash:
            self.hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        return hashlib.sha256(
            f"{self.epoch}{self.parent_hash}{''.join(self.transactions)}".encode()
        ).hexdigest()

class StreamletNode:
    def __init__(self, node_id: int, total_nodes: int):
        self.node_id = node_id
        self.total_nodes = total_nodes
        self.blockchain: List[Block] = []
        self.pending_votes: Dict[str, Set[int]] = {}
        self.init_genesis()
    
    def init_genesis(self):
        genesis = Block(epoch=0, parent_hash="0", transactions=["Genesis"])
        genesis.notarized = True
        genesis.finalized = True
        self.blockchain.append(genesis)
    
    def is_leader(self, epoch: int) -> bool:
        return epoch % self.total_nodes == self.node_id
    
    def propose_block(self, epoch: int) -> Optional[Block]:
        if not self.is_leader(epoch):
            return None
        
        # Get longest notarized chain tip
        tip = self.blockchain[-1]
        transactions = [f"TX{epoch}-{i}" for i in range(3)]  # Demo transactions
        return Block(epoch, tip.hash, transactions)
    
    def validate_block(self, block: Block) -> bool:
        # Validate block structure and parent exists
        parent_exists = any(b.hash == block.parent_hash for b in self.blockchain)
        return (
            parent_exists and
            block.hash == block.calculate_hash() and
            block.epoch > self.blockchain[-1].epoch
        )
    
    def vote_for_block(self, block: Block):
        if self.validate_block(block):
            if block.hash not in self.pending_votes:
                self.pending_votes[block.hash] = set()
            self.pending_votes[block.hash].add(self.node_id)
            
            # Check for notarization (2/3 majority)
            if len(self.pending_votes[block.hash]) >= (2 * self.total_nodes) // 3:
                block.notarized = True
                self.try_finalize(block)
    
    def try_finalize(self, block: Block):
        # Find three consecutive notarized blocks
        chain = self.blockchain.copy()
        chain.append(block)
        
        # Check if we have at least 3 blocks
        if len(chain) < 3:
            return
            
        # Start from the most recent block and go backward
        for i in range(len(chain) - 3, -1, -1):
            if (
                chain[i].notarized and
                chain[i+1].notarized and
                chain[i+2].notarized
            ):
                # Finalize the three consecutive blocks
                for j in range(i, i+3):
                    chain[j].finalized = True
                # Commit finalized chain
                self.blockchain = chain[:i+3]
                return

class StreamletConsensus:
    def __init__(self, num_nodes: int = 4):
        self.nodes = [StreamletNode(i, num_nodes) for i in range(num_nodes)]
        self.epoch = 1
    
    def run_epoch(self):
        # Leader proposes block
        leader = self.nodes[self.epoch % len(self.nodes)]
        new_block = leader.propose_block(self.epoch)
        
        if new_block:
            # Set proposer
            new_block.proposer = leader.node_id
            
            # Broadcast to all nodes
            for node in self.nodes:
                node.vote_for_block(new_block)
        
        self.epoch += 1
    
    def visualize_data(self):
        # Use the first node's blockchain for visualization
        return {
            "blocks": [{
                "epoch": b.epoch,
                "hash": b.hash[:8] if b.hash else "N/A",
                "parent": b.parent_hash[:8] if b.parent_hash else "0",
                "notarized": b.notarized,
                "finalized": b.finalized,
                "proposer": b.proposer,
                "voters": list(b.voters) if b.voters else []
            } for b in self.nodes[0].blockchain]
        }