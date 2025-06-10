class User {
  final String username;
  final String email;
  final String fullName;
  final String location;
  final String? phone;

  User({
    required this.username,
    required this.email,
    required this.fullName,
    required this.location,
    this.phone,
  });

  factory User.fromJson(Map<String, dynamic> json) => User(
        username: json['username'],
        email: json['email'],
        fullName: json['full_name'],
        location: json['location'],
        phone: json['phone'],
      );

  Map<String, dynamic> toJson() => {
        'username': username,
        'email': email,
        'full_name': fullName,
        'location': location,
        'phone': phone,
      };
}
