provider "oci" {
  tenancy_ocid     = ""
  user_ocid        = ""
  fingerprint      = ""
  private_key_path = ""
  region           = "eu-stockholm-1"
}

resource "oci_core_instance" "server" {
  availability_domain = var.AD
  compartment_id      = var.compartment_ocid
  display_name        = "server"
  shape               = var.instance_shape

  create_vnic_details {
    subnet_id      = oci_core_subnet.subnet.id
    display_name   = "server"
    assign_public_ip = true
  }
  
  shape_config {
    memory_in_gbs = "1"
    ocpus         = "1"
  }
  source_details {
    source_type = "image"
    source_id   = var.image_id
  }
  
  metadata = {
    ssh_authorized_keys = chomp(file(var.ssh_public_key))

  }
}

resource "oci_core_vcn" "vcn" {
  compartment_id = var.compartment_ocid
  cidr_block     = "10.0.0.0/16"
  display_name   = "vcn"
  dns_label      = "vcn"
}

resource "oci_core_subnet" "subnet" {
  compartment_id      = var.compartment_ocid
  availability_domain = var.AD
  vcn_id              = oci_core_vcn.vcn.id
  security_list_ids   = [oci_core_security_list.security_list.id]
  route_table_id      = oci_core_route_table.routetable.id
  display_name        = "subnet"
  dns_label           = "subnet"
  cidr_block          = "10.0.0.0/16"
}

resource "oci_core_security_list" "security_list" {
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.vcn.id
  display_name   = "security_list"
  
  egress_security_rules {
    destination = "0.0.0.0/0"
    protocol    = "all"
    stateless   = false
  }
  
  ingress_security_rules {
    source   = "0.0.0.0/0"
    protocol = "6"
    stateless = false
    
    tcp_options {
      max = 22
      min = 22
    }
  }

  ingress_security_rules {
    source   = "0.0.0.0/0"
    protocol = "6"
    stateless = false
    
    tcp_options {
      max = 5000
      min = 5000
    }
  }

  ingress_security_rules {
    source   = "0.0.0.0/0"
    protocol = "1"
    stateless = false

    icmp_options {
      type = 3
      code = 4
    }
  }

  ingress_security_rules {
    source   = "10.0.0.0/16"
    protocol = "1"
    stateless = false

    icmp_options {
      type = 3
    }
  }
}

resource "oci_core_internet_gateway" "gateway" {
  compartment_id = var.compartment_ocid
  display_name   = "gateway"
  vcn_id         = oci_core_vcn.vcn.id
}

resource "oci_core_route_table" "routetable" {
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.vcn.id
  display_name   = "routetable"
  route_rules {
    network_entity_id = oci_core_internet_gateway.gateway.id
    destination       = "0.0.0.0/0"
  }
}