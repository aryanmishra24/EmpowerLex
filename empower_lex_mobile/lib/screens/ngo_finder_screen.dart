import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/ngo_provider.dart';

class NGOFinderScreen extends StatefulWidget {
  const NGOFinderScreen({Key? key}) : super(key: key);

  @override
  _NGOFinderScreenState createState() => _NGOFinderScreenState();
}

class _NGOFinderScreenState extends State<NGOFinderScreen> {
  final TextEditingController _searchController = TextEditingController();
  String _selectedCategory = 'All';
  String _selectedLocation = 'All';
  final List<String> _categories = ['All', 'Legal Aid', 'Women Rights', 'Child Rights', 'Human Rights'];
  final List<String> _locations = ['All', 'Delhi', 'Mumbai', 'Bangalore', 'Chennai', 'Kolkata'];

  @override
  void initState() {
    super.initState();
    _loadNGOs();
  }

  Future<void> _loadNGOs() async {
    final ngoProvider = Provider.of<NGOProvider>(context, listen: false);
    if (_selectedCategory != 'All' && _selectedLocation != 'All') {
      await ngoProvider.getNGOsByCategory(_selectedCategory, location: _selectedLocation);
    } else if (_selectedCategory != 'All') {
      await ngoProvider.getNGOsByCategory(_selectedCategory);
    } else if (_selectedLocation != 'All') {
      await ngoProvider.getNGOsByLocation(_selectedLocation);
    } else {
      await ngoProvider.searchNGOs('');
    }
  }

  Future<void> _searchNGOs(String query) async {
    final ngoProvider = Provider.of<NGOProvider>(context, listen: false);
    if (_selectedCategory != 'All' && _selectedLocation != 'All') {
      await ngoProvider.searchNGOs(query, category: _selectedCategory, location: _selectedLocation);
    } else if (_selectedCategory != 'All') {
      await ngoProvider.searchNGOs(query, category: _selectedCategory);
    } else if (_selectedLocation != 'All') {
      await ngoProvider.searchNGOs(query, location: _selectedLocation);
    } else {
      await ngoProvider.searchNGOs(query);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('NGO Finder'),
      ),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              children: [
                TextField(
                  controller: _searchController,
                  decoration: InputDecoration(
                    hintText: 'Search NGOs...',
                    prefixIcon: Icon(Icons.search),
                    border: OutlineInputBorder(),
                  ),
                  onSubmitted: _searchNGOs,
                ),
                SizedBox(height: 16),
                Row(
                  children: [
                    Expanded(
                      child: DropdownButtonFormField<String>(
                        value: _selectedCategory,
                        decoration: InputDecoration(
                          labelText: 'Category',
                          border: OutlineInputBorder(),
                        ),
                        items: _categories.map((category) {
                          return DropdownMenuItem(
                            value: category,
                            child: Text(category),
                          );
                        }).toList(),
                        onChanged: (value) {
                          if (value != null) {
                            setState(() => _selectedCategory = value);
                            _loadNGOs();
                          }
                        },
                      ),
                    ),
                    SizedBox(width: 16),
                    Expanded(
                      child: DropdownButtonFormField<String>(
                        value: _selectedLocation,
                        decoration: InputDecoration(
                          labelText: 'Location',
                          border: OutlineInputBorder(),
                        ),
                        items: _locations.map((location) {
                          return DropdownMenuItem(
                            value: location,
                            child: Text(location),
                          );
                        }).toList(),
                        onChanged: (value) {
                          if (value != null) {
                            setState(() => _selectedLocation = value);
                            _loadNGOs();
                          }
                        },
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),
          Expanded(
            child: Consumer<NGOProvider>(
              builder: (context, ngoProvider, child) {
                if (ngoProvider.isLoading) {
                  return Center(child: CircularProgressIndicator());
                }

                if (ngoProvider.error != null) {
                  return Center(child: Text(ngoProvider.error!));
                }

                if (ngoProvider.ngos.isEmpty) {
                  return Center(child: Text('No NGOs found'));
                }

                return ListView.builder(
                  itemCount: ngoProvider.ngos.length,
                  itemBuilder: (context, index) {
                    final ngo = ngoProvider.ngos[index];
                    return Card(
                      margin: EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                      child: ListTile(
                        title: Text(ngo.name),
                        subtitle: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text('Contact: ${ngo.contact}'),
                            Text('Email: ${ngo.email}'),
                            Text('Address: ${ngo.address}'),
                            Text('Services: ${ngo.services.join(", ")}'),
                          ],
                        ),
                        trailing: IconButton(
                          icon: Icon(Icons.info),
                          onPressed: () {
                            showDialog(
                              context: context,
                              builder: (context) => AlertDialog(
                                title: Text(ngo.name),
                                content: Column(
                                  mainAxisSize: MainAxisSize.min,
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    Text('Contact: ${ngo.contact}'),
                                    Text('Email: ${ngo.email}'),
                                    Text('Address: ${ngo.address}'),
                                    Text('Services: ${ngo.services.join(", ")}'),
                                    Text('Website: ${ngo.website}'),
                                  ],
                                ),
                                actions: [
                                  TextButton(
                                    onPressed: () => Navigator.pop(context),
                                    child: Text('Close'),
                                  ),
                                ],
                              ),
                            );
                          },
                        ),
                      ),
                    );
                  },
                );
              },
            ),
          ),
        ],
      ),
    );
  }

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }
} 