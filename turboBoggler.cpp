#include <iostream>
#include <fstream>
#include <unordered_map>
#include <unordered_set>
#include <vector>
#include <string>
#include <cmath>
#include <chrono>
#include <algorithm>
#include "boggleTrie.hpp"

using namespace std;
using namespace std::chrono;

using Grid = vector<vector<char>>;

void initGrid(Grid& grid, string gridString) {
    int N = sqrt(gridString.size());
    for (int i = 0; i < N; i++) {
        vector<char> row;
        for (int j = 0; j< N; j++) {
            row.push_back(gridString[i*N+j]);
        }
        grid.push_back(row);
    }
}

void dfs(int y, int x, Grid& grid, TrieNode* trieNode, unordered_set<string>& foundWords) {
    int N = grid.size();
    
    char currentChar = grid[y][x];
    int charIndex = currentChar - 'a';

    TrieNode* nextNode = trieNode->children[charIndex];
    if (nextNode == nullptr) {
        return;
    }

    if (!nextNode->isEnd.empty()) {
        foundWords.insert(nextNode->isEnd);
    }
    
    grid[y][x] = '#';
    static const vector<pair<int, int>> directions = {
        {-1,-1},{-1,0},{-1,1},{0,-1},{0,1},{1,-1},{1,0},{1,1}
    };

    for (auto const& dir : directions) {
        int ny = y + dir.first;
        int nx = x + dir.second;

        if (ny < 0 || nx < 0 || ny >= N || nx >= N || grid[ny][nx] == '#') {
            continue;
        }
        dfs(ny, nx, grid, nextNode, foundWords);
    }
    grid[y][x] = currentChar;
}
void replaceAll(std::string& str, const std::string& from, const std::string& to) {
    if(from.empty())
        return;
    size_t start_pos = 0;
    while((start_pos = str.find(from, start_pos)) != std::string::npos) {
        str.replace(start_pos, from.length(), to);
        start_pos += to.length();
    }
}
int main(int argc, char *argv[]) {
    string wordString = argv[1];
    Grid grid;
    initGrid(grid, wordString);

    int N = grid.size();

    std::ifstream inputFile("wordlist.txt");
    std::string line;
    Trie myTrie = Trie();
    if (inputFile.is_open()) {
        while(std::getline(inputFile, line)) {
            myTrie.insert(line);
        }
        inputFile.close();
    } else {
        cout << "Unable to open file." << endl;
    }
    unordered_set<string> foundWords;
    auto start = high_resolution_clock::now();
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            dfs(i, j, grid, myTrie.root, foundWords);
        }
    }
    auto elapsedTime = high_resolution_clock::now() - start;
    long long microSeconds = duration_cast<microseconds>(elapsedTime).count();
    cout << microSeconds << endl;

    for (string word: foundWords) {
        replaceAll(word, "q", "qu");
        cout << word << endl;
    }
}