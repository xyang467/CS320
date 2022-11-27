# project: p3
# submitter: xyang467
# partner: none
# hours: 10
from collections import deque
import pandas as pd
class GraphSearcher:
    def __init__(self):
        self.visited = set()
        self.order = []

    def go(self, node):
        raise Exception("must be overridden in sub classes -- don't change me here!")

    def dfs_search(self, node):
        self.visited.clear()
        self.order = []
        self.dfs_visit(node)

    def dfs_visit(self, node):
        if node in self.visited:
            return 
        self.visited.add(node)
        self.order.append(node)
        children_list = self.go(node)
        for child in children_list:
            self.dfs_visit(child)
            
    def bfs_search(self, node):
        self.visited.clear()
        self.order = []
        self.bfs_visit(node)
        
    def bfs_visit(self, node):
        todo = deque([node])
        self.visited.add(node)
        self.order.append(node)
        while len(todo)>0:
            curr_node = todo.popleft()
            children_list = self.go(curr_node)
            for child in children_list:
                if child not in self.visited:
                    todo.append(child)
                    self.visited.add(child)
                    self.order.append(child)
            

class MatrixSearcher(GraphSearcher):
    def __init__(self, df):
        super().__init__()
        self.df = df

    def go(self, node):
        children = []
        for n, has_edge in self.df.loc[node].items():
            if has_edge == 1:
                children.append(n)
        return children

class FileSearcher(GraphSearcher):
    def __init__(self):
        super().__init__()
        self.val = ''
    def go(self, file):
        with open(f"file_nodes/{file}") as f:
            text = f.read()
            children_list = text.strip().split("\n")[-1].split(",")
            self.val += text.strip().split("\n")[0]
            return children_list
    def message(self):
        return self.val
    
class WebSearcher(GraphSearcher):
    def __init__(self,driver):
        super().__init__()
        self.driver = driver
        self.dfs = []
        
    def go(self,url):
        self.driver.get(url)
        dfs = pd.read_html(self.driver.page_source)
        self.dfs.append(dfs[0])
        children = []
        links = self.driver.find_elements(by="tag name", value="a")
        for link in links:
            child_url = link.get_attribute("href")
            children.append(child_url)
        return children

    def table(self):
        df = pd.concat(self.dfs,ignore_index=True)
        return df

    
from selenium.common.exceptions import NoSuchElementException
import time
import requests

def reveal_secrets(driver,url,travellog):
    password = ''
    for i in travellog.clue:
        password += str(i)
    driver.get(url)
    driver.find_element(value="password").send_keys(password)
    driver.find_element(value="attempt-button").click()
    attempts = 10
    for _ in range(attempts):
        try:
            driver.find_element(value="securityBtn").click()
            break
        except NoSuchElementException:
            time.sleep(0.2)
            
    for _ in range(attempts):
        try:
            jpg_url = driver.find_element(value="image").get_attribute("src") 
            # adapted from https://www.adamsmith.haus/python/answers/how-to-download-an-image-using-requests-in-python#:~:text=Use%20requests.,write%2Dand%2Dbinary%20mode.
            response = requests.get(jpg_url)
            file = open("Current_Location.jpg", "wb")
            file.write(response.content)
            file.close()
            location = driver.find_element(value="location").text
            break
        except NoSuchElementException:
            time.sleep(0.2)
    return location
