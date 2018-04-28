import os.path
import sqlite3
from helpers.b_dir_earch import findTheWikiConnection 


class Database:
    """
        DB connection
    """

    def __init__(self, DBArchive_path="./fuse.sqlite"):

        if not os.path.isfile(DBArchive_path):
            raise IOError('{} does not exist'.format(DBArchive_path))

        self.__connection = sqlite3.connect(DBArchive_path, check_same_thread=False)
        self.__curr = self.__connection.cursor()
        

    def find_outgoing(self, arr):
        """
            Takes an array of ids and returns all outgoing links
            for each elem
        """
        query = "SELECT id, outgoing_links FROM links WHERE id IN {}"
        # print(query)
        res = self.__curr.execute(query.format(str(tuple(arr)).replace(',)', ')')))
        return {row[0]: row[1].split("|") for row in res}
        

    def find_incoming(self, arr):
        """
            Takes an array of ids and returns all incoming links
            for each elem
        """
        query = "SELECT id, incoming_links FROM links WHERE id IN {}"
        # print(query)
        res = self.__curr.execute(query.format(str(tuple(arr)).replace(',)', ')')))
        return {row[0]: row[1].split("|") for row in res}

    def matrix_ids_to_titles(self, matrix):
        return [self.find_titles(row) for row in matrix]

    def find_title(self, page_id):
        query = "SELECT title FROM pages WHERE id={}"
        return [row for row in self.__curr.execute(query.format(page_id))][0]
     


    def find_titles(self, arr):
        return [self.find_title(page_id) for page_id in arr]

    def test(self, source_id, target_id):
        return self.matrix_ids_to_titles(findTheWikiConnection(self, source_id, target_id))


    def close(self):
        self.__connection.close()