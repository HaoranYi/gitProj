// inside App_Start

using System.Web;
using System.Web.Optimization;
using System.Web.Optimization.React;

namespace FirstReactApp
{
    public class BundleConfig
    {
        // For more information on bundling, visit https://go.microsoft.com/fwlink/?LinkId=301862
        public static void RegisterBundles(BundleCollection bundles)
        {

            bundles.Add(new BabelBundle("~/bundles/main").Include(
                        "~/Scripts/react/ProductList.jsx"));
        }
    }
}
