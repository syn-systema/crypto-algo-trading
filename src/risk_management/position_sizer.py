"""
Risk Management Module for Crypto Trading
Based on Day 5.1 - Coding Risk Management from Moon Dev's Algo Trade Camp
"""

from typing import Dict, Optional
from decimal import Decimal
import logging
from ..config import (
    MAX_POSITION_SIZE,
    STOP_LOSS_PERCENTAGE,
    TAKE_PROFIT_PERCENTAGE
)

logger = logging.getLogger(__name__)

class PositionSizer:
    def __init__(self, account_balance: float, max_risk_per_trade: float = 0.02):
        """
        Initialize the Position Sizer
        
        Args:
            account_balance: Total account balance in USDT
            max_risk_per_trade: Maximum risk per trade as a decimal (default 2%)
        """
        self.account_balance = Decimal(str(account_balance))
        self.max_risk_per_trade = Decimal(str(max_risk_per_trade))
        
    def calculate_position_size(self, entry_price: float, stop_loss: float) -> Dict:
        """
        Calculate the optimal position size based on account risk management rules
        
        Args:
            entry_price: Intended entry price
            stop_loss: Stop loss price
            
        Returns:
            Dict containing position size and risk metrics
        """
        entry_price = Decimal(str(entry_price))
        stop_loss = Decimal(str(stop_loss))
        
        # Calculate risk per unit
        risk_per_unit = abs(entry_price - stop_loss)
        
        # Calculate maximum loss allowed
        max_loss = self.account_balance * self.max_risk_per_trade
        
        # Calculate position size
        position_size = max_loss / risk_per_unit
        
        # Calculate position value
        position_value = position_size * entry_price
        
        # Ensure position size doesn't exceed max allowed percentage of account
        max_position_value = self.account_balance * Decimal(str(MAX_POSITION_SIZE))
        if position_value > max_position_value:
            position_size = max_position_value / entry_price
            position_value = position_size * entry_price
        
        return {
            'position_size': float(position_size),
            'position_value': float(position_value),
            'risk_amount': float(max_loss),
            'risk_percentage': float(self.max_risk_per_trade * 100),
            'account_size_used': float(position_value / self.account_balance * 100)
        }
    
    def calculate_take_profit(self, entry_price: float, risk_reward_ratio: float = 2.0) -> float:
        """
        Calculate take profit price based on risk-reward ratio
        
        Args:
            entry_price: Entry price of the position
            risk_reward_ratio: Desired risk/reward ratio (default 2.0)
            
        Returns:
            Take profit price
        """
        entry_price = Decimal(str(entry_price))
        risk = entry_price * Decimal(str(STOP_LOSS_PERCENTAGE))
        reward = risk * Decimal(str(risk_reward_ratio))
        
        return float(entry_price + reward)
    
    def validate_trade(self, entry_price: float, stop_loss: float, 
                      take_profit: float, side: str) -> Dict:
        """
        Validate if a trade meets risk management criteria
        
        Args:
            entry_price: Entry price of the position
            stop_loss: Stop loss price
            take_profit: Take profit price
            side: Trade direction ('long' or 'short')
            
        Returns:
            Dict containing validation results and metrics
        """
        entry_price = Decimal(str(entry_price))
        stop_loss = Decimal(str(stop_loss))
        take_profit = Decimal(str(take_profit))
        
        # Calculate risk and reward
        if side.lower() == 'long':
            risk = (entry_price - stop_loss) / entry_price
            reward = (take_profit - entry_price) / entry_price
        else:  # short
            risk = (stop_loss - entry_price) / entry_price
            reward = (entry_price - take_profit) / entry_price
            
        risk_reward_ratio = reward / risk if risk != 0 else 0
        
        # Validate trade parameters
        position_metrics = self.calculate_position_size(entry_price, stop_loss)
        
        return {
            'valid': all([
                risk <= Decimal(str(STOP_LOSS_PERCENTAGE)),
                risk_reward_ratio >= Decimal('1.5'),
                position_metrics['account_size_used'] <= float(MAX_POSITION_SIZE * 100)
            ]),
            'risk_percentage': float(risk * 100),
            'reward_percentage': float(reward * 100),
            'risk_reward_ratio': float(risk_reward_ratio),
            'position_metrics': position_metrics
        }
    
    def adjust_position_for_leverage(self, position_size: float, 
                                  leverage: float = 1.0) -> float:
        """
        Adjust position size for leveraged trading
        
        Args:
            position_size: Original position size
            leverage: Leverage multiplier (default 1.0 for spot trading)
            
        Returns:
            Adjusted position size
        """
        if leverage <= 0:
            raise ValueError("Leverage must be greater than 0")
            
        return position_size * leverage
