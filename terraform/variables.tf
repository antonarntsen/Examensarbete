variable "AD" {
  type        = string
  default     = "OMUz:EU-STOCKHOLM-1-AD-1"
}

variable "image_id" {
  type        = string
  default     = "ocid1.image.oc1.eu-stockholm-1.aaaaaaaaiq7jscj64rljs4pmhr6usaib6wn7agcrlp67zexvq5p256crdjfq"
}

variable "compartment_ocid" {
  type        = string
  default     = ""
}

variable "ssh_public_key" {
  type        = string
  default     = "ssh-key.pub"
}

variable "instance_shape" {
  type        = string
  default     = "VM.Standard.E2.1.Micro"
}