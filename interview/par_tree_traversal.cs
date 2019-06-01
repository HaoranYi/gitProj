// use parallel task to traverse trees
public class TreeWalk
{
    static void Main()
    {
        Tree<MyClass> tree = new Tree<MyClass>();

        // ...populate tree

        // define the action to perform on each node
        Action<MyClass> myAction = x => Console.WriteLine("{0} : {1}", x.Name, x.Number);

        // Traverse the tree with parallel tasks
        DoTree(tree, myAction);
    }

    public class MyClass
    {
        public string Name { get; set; }
        public int Number { get; set; }
    }

    public class Tree<T>
    {
        public Tree<T> Left;
        public Tree<T> Right;
        public T Data;
    }

    public static void DoTree<T>(Tree<T> tree, Action<T> action)
    {
        if (tree == null) return;
        var left = Task.Factory.StartNew(()=>DoTree(tree.Left, action));
        var right = Task.Factory.StartNew(()=>DoTree(tree.Right, action));
        ation(tree.Data);

        try
        {
            Task.WaitAll(left, right);
        }
        catch (AggregateException)
        {
            // handle exceptions here
        }
    }

    public static void DoTree2<T>(Tree<T> tree, Action<T> action)
    {
        if (tree == null) return;
        Parallel.Invoke(
                () => DoTree2(tree.Left, action);
                () => DoTree2(tree.Right, action);
                () => action(tree.Data);
                );
    }
}
