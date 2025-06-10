import 'package:flutter/material.dart';

class CaseFilter extends StatelessWidget {
  final String selectedFilter;
  final Function(String) onFilterChanged;

  const CaseFilter({
    Key? key,
    required this.selectedFilter,
    required this.onFilterChanged,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      child: SingleChildScrollView(
        scrollDirection: Axis.horizontal,
        child: Row(
          children: [
            ChoiceChip(
              label: Text('All'),
              selected: selectedFilter == 'all',
              onSelected: (selected) => onFilterChanged('all'),
              backgroundColor: Colors.grey[200],
              selectedColor: Theme.of(context).primaryColor.withOpacity(0.2),
              labelStyle: TextStyle(
                color: selectedFilter == 'all' ? Theme.of(context).primaryColor : Colors.black87,
                fontWeight: selectedFilter == 'all' ? FontWeight.bold : FontWeight.normal,
              ),
            ),
            SizedBox(width: 8),
            ChoiceChip(
              label: Text('Pending'),
              selected: selectedFilter == 'pending',
              onSelected: (selected) => onFilterChanged('pending'),
              backgroundColor: Colors.grey[200],
              selectedColor: Theme.of(context).primaryColor.withOpacity(0.2),
              labelStyle: TextStyle(
                color: selectedFilter == 'pending' ? Theme.of(context).primaryColor : Colors.black87,
                fontWeight: selectedFilter == 'pending' ? FontWeight.bold : FontWeight.normal,
              ),
            ),
            SizedBox(width: 8),
            ChoiceChip(
              label: Text('In Progress'),
              selected: selectedFilter == 'in_progress',
              onSelected: (selected) => onFilterChanged('in_progress'),
              backgroundColor: Colors.grey[200],
              selectedColor: Theme.of(context).primaryColor.withOpacity(0.2),
              labelStyle: TextStyle(
                color: selectedFilter == 'in_progress' ? Theme.of(context).primaryColor : Colors.black87,
                fontWeight: selectedFilter == 'in_progress' ? FontWeight.bold : FontWeight.normal,
              ),
            ),
            SizedBox(width: 8),
            ChoiceChip(
              label: Text('Completed'),
              selected: selectedFilter == 'completed',
              onSelected: (selected) => onFilterChanged('completed'),
              backgroundColor: Colors.grey[200],
              selectedColor: Theme.of(context).primaryColor.withOpacity(0.2),
              labelStyle: TextStyle(
                color: selectedFilter == 'completed' ? Theme.of(context).primaryColor : Colors.black87,
                fontWeight: selectedFilter == 'completed' ? FontWeight.bold : FontWeight.normal,
              ),
            ),
          ],
        ),
      ),
    );
  }
} 