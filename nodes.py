from flask import Flask, jsonify, request
import requests
import random

node_limit = 10

node_clusters = []

clusterA = {
    "http://192.168.0.23:5000", #Ani
    "http://192.168.0.23:5001", #Martin
    "http://192.168.0.23:5002"  #Tamarcus
}

node_clusters.append(clusterA)

class Nodes:
    #Only returning clusterA for now since it is the only one that exists
    @staticmethod
    def select_random_cluster() :
        return clusterA

    #selecting the nodes from a cluster to take on the transaction
    @staticmethod
    def push_transaction(transaction) : 
        selected_cluster = Nodes.select_random_cluster
        pushed_nodes = random.sample(selected_cluster, 2)
        for node in pushed_nodes:
            requests.get(node + '/addTransaction')
    