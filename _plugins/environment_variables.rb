# Jekyll plugin to load environment variables into site config
# This allows us to access environment variables in templates

Jekyll::Hooks.register :site, :after_init do |site|
  # Load CHATBOT_API_URL from environment if present
  if ENV['CHATBOT_API_URL']
    puts "Loading CHATBOT_API_URL: #{ENV['CHATBOT_API_URL']}"
    site.config['chatbot_api_url'] = ENV['CHATBOT_API_URL']
    puts "Site config chatbot_api_url set to: #{site.config['chatbot_api_url']}"
  else
    puts "CHATBOT_API_URL environment variable not found"
  end
end
