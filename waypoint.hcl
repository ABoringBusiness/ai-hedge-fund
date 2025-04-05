project = "ai-hedge-fund"

app "ai-hedge-fund" {
  build {
    use "docker" {
      dockerfile = "Dockerfile"
    }
    
    registry {
      use "docker" {
        image = "ai-hedge-fund"
        tag   = "latest"
        local = true
      }
    }
  }

  deploy {
    use "kubernetes" {
      probe_path = "/"
      
      service_port = 80
      
      namespace = "default"
      
      pod {
        container {
          name = "ai-hedge-fund"
          
          args = [
            "--tickers", "AAPL,MSFT,GOOGL",
            "--show-reasoning"
          ]
          
          env {
            name = "PYTHONUNBUFFERED"
            value = "1"
          }
          
          resources {
            cpu {
              request = "500m"
              limit   = "1000m"
            }
            memory {
              request = "1Gi"
              limit   = "2Gi"
            }
          }
        }
      }
    }
  }

  release {
    use "kubernetes" {
      namespace = "default"
      
      load_balancer = false
    }
  }
}

variable "api_keys" {
  default = {}
  type = map(string)
  sensitive = true
}

# Example usage:
# waypoint up -var="api_keys={\"OPENAI_API_KEY\":\"sk-...\",\"ANTHROPIC_API_KEY\":\"sk-...\"}"