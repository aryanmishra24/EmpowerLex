import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'providers/user_provider.dart';
import 'providers/case_provider.dart';
import 'providers/ngo_provider.dart';
import 'services/api_service.dart';
import 'services/auth_service.dart';
import 'screens/login_screen.dart';
import 'screens/dashboard_screen.dart';

void main() {
  final apiService = ApiService();
  final authService = AuthService(apiService: apiService);
  runApp(MyApp(apiService: apiService, authService: authService));
}

class MyApp extends StatelessWidget {
  final ApiService apiService;
  final AuthService authService;
  const MyApp({Key? key, required this.apiService, required this.authService}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => UserProvider(authService: authService)),
        ChangeNotifierProvider(create: (_) => CaseProvider(apiService: apiService)),
        ChangeNotifierProvider(create: (_) => NGOProvider(apiService: apiService)),
      ],
      child: MaterialApp(
        title: 'EmpowerLex',
        debugShowCheckedModeBanner: false,
        theme: ThemeData(
          primarySwatch: Colors.blue,
          visualDensity: VisualDensity.adaptivePlatformDensity,
        ),
        home: Consumer<UserProvider>(
          builder: (context, userProvider, _) {
            // Only show loading indicator during initial load
            if (userProvider.isLoading && userProvider.user == null) {
              return Scaffold(
                body: Center(child: CircularProgressIndicator()),
              );
            }
            
            // If not logged in, show login screen
            if (!userProvider.isLoggedIn) {
              return LoginScreen();
            }
            
            // If logged in, show dashboard
            return DashboardScreen();
          },
        ),
      ),
    );
  }
}
