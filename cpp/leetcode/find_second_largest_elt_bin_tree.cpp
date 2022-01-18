// find the second larget element in a binary search tree.

struct Node {
    Node* left;
    Node* right;
    int data;
};

void find_right_most_node(Node* root, Node** right, Node** parent)
{
    *parent = nullptr;
    *right = root;
    if (root == nullptr)
    {
        *right = nullptr;
        return;
    }
    Node* p = root;
    while (p->right != nullptr)
    {
        *parent = p;
        p = p->right;
    }
    *right = p;
}

Node* find_second_larget_node(Node* root)
{
    if (root == nullptr)
        return nullptr;

    Node* right;
    Node* parent;
    find_right_most_node(root, &right, &parent);

    // if right most node is a leaf node, return parent node.
    if (right->left == nullptr)
    {
        return parent;
    }

    // if right->left != nullptr, return right most node of left subtree
    find_right_most_node(right->left, &right, &parent);
    return right;
}
