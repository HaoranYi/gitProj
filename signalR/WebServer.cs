/* packages used on the server

<PackageReference Include="Microsoft.AspNetCore.Cors" Version="2.0.1" />
<PackageReference Include="Microsoft.AspNetCore.Diagnostics" Version="2.0.1" />
<PackageReference Include="Microsoft.AspNetCore.Hosting" Version="2.0.1" />
<PackageReference Include="Microsoft.AspNetCore.Server.Kestrel" Version="2.0.1" />
<PackageReference Include="Microsoft.AspNetCore.SignalR" Version="1.0.0-alpha2-final" />
<PackageReference Include="Microsoft.AspNetCore.StaticFiles" Version="2.0.1" />
<PackageReference Include="Microsoft.Extensions.Configuration.CommandLine" Version="2.0.0" />
<PackageReference Include="Microsoft.Extensions.Logging.Console" Version="2.0.0" />
*/
using System.IO;
using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;

namespace SignalRSample.Web
{
    public class Program
    {
        static void Main(string[] args)
        {
            var config = new ConfigurationBuilder()
                .AddCommandLine(args)
                .Build();

            var host = new WebHostBuilder()
                .UseConfiguration(config)
                .UseSetting(WebHostDefaults.PreventHostingStartupKey, "true")
                .ConfigureLogging(factory =>
                {
                    factory.AddConsole();
                })
                .UseKestrel()
                .UseContentRoot(Directory.GetCurrentDirectory())
                .UseEnvironment("Development")
                .UseStartup<Startup>()
                .Build();

            host.Run();
        }
    }
}
