using System;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.AspNetCore.SignalR.Client;
using Microsoft.Extensions.Logging;
using SignalRSample.Core.Models;

namespace SignalRSample.ConsoleApp
{
    public class Program
    {
        private static readonly ILogger logger = CreateLogger("Program");

        public static void Main(string[] args)
        {
            var cancellationTokenSource = new CancellationTokenSource();

            Task.Run(() => MainAsync(cancellationTokenSource.Token).GetAwaiter().GetResult(), cancellationTokenSource.Token);

            Console.WriteLine("Press Enter to Exit ...");
            Console.ReadLine();

            cancellationTokenSource.Cancel();
        }

        private static async Task MainAsync(CancellationToken cancellationToken)
        {
            var hubConnection = new HubConnectionBuilder()
                .WithUrl("http://localhost:5000/sensor")
                .Build();

            await hubConnection.StartAsync();

            // Initialize a new Random Number Generator:
            Random rnd = new Random();

            double value = 0.0d;

            while (!cancellationToken.IsCancellationRequested)
            {
                await Task.Delay(250, cancellationToken);

                // Generate the value to Broadcast to Clients:
                value = Math.Min(Math.Max(value + (0.1 - rnd.NextDouble() / 5.0), -1), 1);

                // Create the Measurement with a Timestamp assigned:
                var measurement = new Measurement() {Timestamp = DateTime.UtcNow, Value = value};

                // Log informations:
                if (logger.IsEnabled(LogLevel.Trace))
                {
                    Console.WriteLine("Broadcasting Measurement to Clients ({0})", measurement);
                }

                // Finally send the value:
                await hubConnection.InvokeAsync("Broadcast", "Sensor", measurement, cancellationToken);
            }

            await hubConnection.DisposeAsync();
        }

        private static ILogger CreateLogger(string loggerName)
        {
            return new LoggerFactory()
                .AddConsole(LogLevel.Trace)
                .CreateLogger(loggerName);
        }
    }
}
