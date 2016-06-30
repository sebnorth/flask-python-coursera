# Mini-project 1 for Principles of Computing class

# based on the template from: http://www.codeskulptor.org/#poc_clicker_template.py

"""
Cookie Clicker Simulator
"""

import simpleplot

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

import math
import random

# Constants
# SIM_TIME = 10000000000.0
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self._total_resources = 0.0
        self._current_resources = 0.0
        self._current_time = 0.0
        self._cps = 1.0
        self._history = [(0.0, None, 0.0, 0.0)]
        
    def __str__(self):
        """
        Return human readable state
        """
        napis = "Time: " + str(self._current_time) + "\n"
        napis += "Current Cookies: " + str(self._current_resources ) + "\n"
        napis += "CPS: " + str(self._cps) + "\n"
        napis += "Total Cookies: " + str(self._total_resources )
        return napis
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._current_resources
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._current_time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: (0.0, None, 0.0, 0.0)
        """
        return self._history

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if self._current_resources >= cookies:
            return 0.0
        else:
            return math.ceil((cookies - self._current_resources )/self._cps)
      
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0
        """
        if time <= 0:
            pass
        else:
            self._current_time+=time
            self._current_resources+=self._cps*time
            self._total_resources+=self._cps*time
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        you should appropriately adjust the current number of cookies, 
        the CPS, and add an entry into the history. 
        """
        if  self._current_resources < cost:
            pass
        else:
            self._current_resources-=cost
            self._cps+=additional_cps
            self._history.extend([(self._current_time, item_name, cost, self._total_resources)])
   
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to game.
    """

    build_info_clone =  build_info.clone()
    clicker = ClickerState()
    while clicker.get_time() <= duration:
        time_left = duration - clicker.get_time() 
        item = strategy(clicker.get_cookies(), clicker.get_cps(), time_left, build_info_clone)
        if item is None:
            clicker.wait(time_left)
            break
        cost_item = build_info_clone.get_cost(item)
        if clicker.get_cookies() >= cost_item:
            pass
        else:
            time_need = clicker.time_until(cost_item)
            if time_need > time_left:
                clicker.wait(time_left)
                break
            else:
                clicker.wait(time_need)
                clicker.buy_item(item, cost_item, build_info_clone.get_cps(item))
                build_info_clone.update_item(item)

    return clicker


def strategy_cursor(cookies, cps, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic strategy does not properly check whether
    it can actually buy a Cursor in the time left.  Your strategy
    functions must do this and return None rather than an item you
    can't buy in the time left.
    """
    return "Cursor"

def strategy_none(cookies, cps, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that you can use to help debug
    your simulate_clicker function
    """
    return None

def strategy_cheap(cookies, cps, time_left, build_info):
    """
    This strategy returns the cheapest possible item
    """
    koszty = [build_info.get_cost(klucz) for klucz in build_info.build_items()]
    koszty.sort()
    min_koszt = -1
    napis = ''
    if koszty[0] <= cookies + time_left*cps:
            min_koszt = koszty[0]
    if min_koszt == -1:
        return None
    else:
        for klucz in build_info.build_items():
            if build_info.get_cost(klucz) == min_koszt:
                napis = klucz
                break
    return napis


def strategy_expensive(cookies, cps, time_left, build_info):
    """
    This strategy returns the most expensive possible item
    """
    koszty = [build_info.get_cost(klucz) for klucz in build_info.build_items()]
    koszty.sort()
    koszty_len = len(koszty)
    napis = ''
    mam = cookies + time_left*cps
    for licznik in range(koszty_len-1,-1,-1):
        if koszty[licznik] <= mam:
            break
    if koszty[0] > mam:
        return None
    else:
        for klucz in build_info.build_items():
            if build_info.get_cost(klucz) == koszty[licznik]:
                napis = klucz
                break
    return napis

def strategy_best(cookies, cps, time_left, build_info):
    """
    This is my best but random strategy :)
    """
    koszty = build_info.build_items()
    koszty_len = len(koszty)
    numer_losowy = random.randrange(0, koszty_len)
    przedmiot = koszty[numer_losowy]
    if build_info.get_cost(przedmiot) > cookies + time_left*cps:
            return None
    return przedmiot
        
    
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation with one strategy
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    # history = state.get_history()
    # history = [(item[0], item[3]) for item in history]
    # simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    run_strategy("Cursor", SIM_TIME, strategy_cursor)
    run_strategy("None", SIM_TIME, strategy_none)
    
    # Add calls to run_strategy to run additional strategies
    # run_strategy("Cheap", SIM_TIME, strategy_cheap)
    # run_strategy("Expensive", SIM_TIME, strategy_expensive)
    # run_strategy("Best", SIM_TIME, strategy_best)
    
run()

