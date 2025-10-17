#include <string>
#include <unordered_map>
#include <array>

#ifndef BOGGLETRIE_HPP
#define BOGGLETRIE_HPP

class TrieNode {
public:
    std::array<TrieNode*, 26> children{};
    std::string isEnd = "";
    TrieNode() = default;
};

class Trie {
public:
    TrieNode* root;
    Trie();

    void insert(std::string word);
    bool search(std::string word);
};


#endif