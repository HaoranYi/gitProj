using System;
using Newtonsoft.Json;

namesapce SignalRSample.Core.Models
{
    public class Measurement
    {
        [JsonProperty("timestamp")]
        public DateTime Timestamp { get; set; }

        [JsonProperty("value")]
        public double value { get; set; }

        public override string ToString()
        {
            return string.Format("Measurement(Timestamp={0}, Value={1})");
        }
    }
}


