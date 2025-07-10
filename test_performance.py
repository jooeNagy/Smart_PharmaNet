import os
import django
import time

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartPharmacy.settings')
django.setup()

from medicine.models import Medicine

def test_medicine_performance():
    print("Testing Medicine model performance...")
    
    # Test 1: Count query
    start = time.time()
    count = Medicine.objects.count()
    end = time.time()
    print(f"Count query: {end - start:.3f} seconds ({count} records)")
    
    # Test 2: Simple query
    start = time.time()
    medicines = list(Medicine.objects.all()[:10])
    end = time.time()
    print(f"Simple query (10 records): {end - start:.3f} seconds")
    
    # Test 3: Optimized query
    start = time.time()
    medicines = list(Medicine.objects.select_related('pharmacy')[:10])
    end = time.time()
    print(f"Optimized query (10 records): {end - start:.3f} seconds")
    
    # Test 4: Search query
    start = time.time()
    medicines = list(Medicine.objects.filter(name__icontains='a')[:10])
    end = time.time()
    print(f"Search query (10 records): {end - start:.3f} seconds")

if __name__ == "__main__":
    test_medicine_performance()