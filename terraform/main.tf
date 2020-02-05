provider "google" {
  credentials = "${file("credentials/gcloud.json")}"
  project = "${jsondecode(file("credentials/gcloud.json"))["project_id"]}"
  region = "${var.region}"
  zone = "${var.zone}"
}

resource "random_id" "announcements" {
  byte_length = 8
}

resource "tls_private_key" "connection_key" {
  algorithm = "RSA"
  rsa_bits = 4096
}

resource "google_compute_network" "announcements_network" {
  name = "announcement-network"
}

resource "google_compute_firewall" "announcements_firewall" {
  name = "announcements-firewall"
  network = "${google_compute_network.announcements_network.name}"

  allow {
    protocol = "tcp"
    ports = [
      "22",
      "80",
      "443"]
  }
}

resource "google_compute_address" "announcements_ip" {
  name = "annoucement-address"
}

resource "google_compute_instance" "announcement" {
  name = "announcement-${random_id.announcements.hex}"
  machine_type = "n1-standard-1"

  boot_disk {
    initialize_params {
      image = "gce-uefi-images/ubuntu-1804-lts"
    }
  }

  scratch_disk {
  }

  provisioner "file" {
    source = "token.pickle"
    destination = "token.pickle"

    connection {
      type = "ssh"
      user = "root"
      host = "${google_compute_instance.announcement.network_interface.0.access_config.0.nat_ip}"
      private_key = "${tls_private_key.connection_key.private_key_pem}"
    }
  }

  metadata_startup_script = "${file("./scripts/announcement-setup.sh")}"

  network_interface {
    network = "${google_compute_network.announcements_network.name}"
    access_config {
      nat_ip = "${google_compute_address.announcements_ip.address}"
    }
  }

  metadata = {
    ssh-keys = "root:${tls_private_key.connection_key.public_key_openssh}"
  }
}

output "announcement-ip" {
  value = "${google_compute_address.announcements_ip.address}"
}