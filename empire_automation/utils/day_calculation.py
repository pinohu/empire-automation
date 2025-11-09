"""
Utility functions for calculating day numbers in the 90-day plan.
"""

import os
import logging
from datetime import date, datetime
from typing import Optional

logger = logging.getLogger(__name__)


def get_plan_start_date() -> date:
    """
    Get the 90-day plan start date from environment variable.
    
    Returns:
        Start date, defaults to today if not set
    """
    start_date_str = os.getenv("PLAN_START_DATE")
    if start_date_str:
        try:
            return datetime.strptime(start_date_str, "%Y-%m-%d").date()
        except ValueError:
            logger.warning(f"Invalid PLAN_START_DATE format: {start_date_str}, using today")
    
    # Default to today if not set
    return date.today()


def calculate_day_number(start_date: Optional[date] = None, current_date: Optional[date] = None) -> int:
    """
    Calculate the current day number in the 90-day plan.
    
    Args:
        start_date: Plan start date (defaults to PLAN_START_DATE env var or today)
        current_date: Current date (defaults to today)
        
    Returns:
        Day number (1-90), or 1 if before start date, or 90 if after plan end
    """
    if start_date is None:
        start_date = get_plan_start_date()
    
    if current_date is None:
        current_date = date.today()
    
    # Calculate days since start
    delta = (current_date - start_date).days
    
    # Day 1 is the first day (start_date)
    day_number = delta + 1
    
    # Clamp to valid range
    if day_number < 1:
        return 1
    elif day_number > 90:
        return 90
    
    return day_number


def calculate_days_remaining(day_number: Optional[int] = None) -> int:
    """
    Calculate days remaining in the 90-day plan.
    
    Args:
        day_number: Current day number (calculated if not provided)
        
    Returns:
        Days remaining (0-89)
    """
    if day_number is None:
        day_number = calculate_day_number()
    
    days_remaining = 90 - day_number
    return max(0, days_remaining)

