# Shoppy Discord Bot
Recently an friend of mine asked me to code an Discord Bot which would automatically give the role to an user when they enter **.verify {order-id}**. The order-id is provided by Shoppy *"when an user purchased an product through shoppy.gg page they will automatically receive an order-id"*. When the user enters the **.verify {order-id}** the user discord id, order-id and the product name is stored in an MySQL server. And if someone else tries to use an order-id which has been used an error will be thrown.

## Setup
Setting up the Discord Bot is really easy all you need to do is to create an config.json, shoppyitems.json, shoppyroles.json.

### Config.json

```` 
  "api"                 : "shoppy-api-key",
  "database_ip"         : "mysql-ip",
  "database_user"       : "mysql-username",
  "database_password"   : "mysql-password"
```` 
### ShoppyItems.json
```` 
  "product-name"       : "product-id",
  "product-name"       : "product-id",
  "product-name"       : "product-id",
  "product-name"       : "product-id"
```` 
### ShoppyRoles.json
```` 
  "product-name"       : "discord-role-id",
  "product-name"       : "discord-role-id",
  "product-name"       : "discord-role-id",
  "product-name"       : "discord-role-id"
````

