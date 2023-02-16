output "vm_id" {
  value = azurerm_virtual_machine.main.id
}

output "vm_ip" {
  value = azurerm_public_ip.myvm1publicip.ip_address
}

output "admin_password" {
  value     = random_password.password.result
  sensitive = true
}