#include <iostream>
#include <string>
#include <unordered_map>
#include <vector>
#include "boggleTrie.hpp"


Trie::Trie() {
    root = new TrieNode();
}

void Trie::insert(std::string word) {
    TrieNode* node = root;
    for (char c : word) {
        int index = c - 'a';
        if (!node->children[index]) {
            node->children[index] = new TrieNode();
        }
        node = node->children[index];
    }
    node->isEnd = word;
}