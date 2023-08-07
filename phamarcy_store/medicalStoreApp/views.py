from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from medicalStoreApp.serializers import CompanySerliazer, CompanyBankSerializer, MedicalDetailsSerializerSimple, MedicineSerliazer,MedicalDetailsSerializer


# Create your views here.
from medicalStoreApp.models import Company, CompanyBank, MedicalDetails, Medicine
#from medicalStoreApp.serializers import CompanySerliazer, CompanyBankSerializer

class CompanyViewSet(viewsets.ViewSet):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]  

    def list(self,request):
        company=Company.objects.all()
        serializer=CompanySerliazer(company,many=True, context={"request", request})
        response_dict={"error": False, "message": "All Company List Data", "data":serializer.data}
        return Response(response_dict)

    def create(self,request):

        try:
            serializer=CompanySerliazer(data=request.data, context={"request":request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response={"error":False,"message":"Company data saved successfully"}
        except:
            dict_response={"error":True,"message":"Error occured while saving company data"}
        return Response(dict_response)

    def update(self, request, pk=None):
        try:
            queryset=Company.objects.all()
            company=get_object_or_404(queryset,pk=pk)
            serializer=CompanySerliazer(company, data=request, context={"request":request})
            serializer.is_valid(raise_exception=True)#
            serializer.save()
            dict_response={"error":False, "message": "Successfully Updated Company Data"}
        except:
            dict_response={"error":True, "message": "An error occured while updating Company data"}

        return Response(dict_response)


class CompanyBankViewset(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
  
    def create(self,request):
        try:
            serializer=CompanyBankSerializer(data=request.data,context={"request":request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response={"error":False,"message":"Company Bank Data Saved Successfully"}
        except:
            dict_response={"error":True,"message":"Error while Saving Company Bank Data"}
        return Response(dict_response)
    
    def list(self,request):
        companyBank=CompanyBank.objects.all()
        serializer=CompanyBankSerializer(companyBank,many=True, context={"request", request})
        response_dict={"error": False, "message": "All Company Bank List Data", "data":serializer.data}
        return Response(response_dict)    
    
    def retrieve(self, request, pk=None):
        queryset=CompanyBank.objects.all()
        companybank=get_object_or_404(queryset, pk=pk)
        serializer=CompanyBankSerializer(companybank, context={"request":request})
        return Response({"error":False, "message": "single data fetched", "data":serializer.data})

    def update(self, request, pk=None):
        queryset=CompanyBank.objects.all()
        companybank=get_object_or_404(queryset, pk=pk)
        serializer=CompanyBankSerializer(companybank,data=request.data, context={"request":request})
        serializer.is_valid()
        serializer.save()
        return Response({"error":False, "message":"Data has been Updated"})
    
class CompanyNameViewSet(generics.ListAPIView):
    serializer_class = CompanySerliazer
    def get_queryset(self):
        name=self.kwargs["name"]
        return Company.objects.filter(name=name)
    

class MedicineViewset(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
  
    def create(self,request):
        try:
            serializer=MedicineSerliazer(data=request.data,context={"request":request})
            serializer.is_valid(raise_exception=True)
            serializer.save()

            medicine_id=serializer.data['id']
            #print(medicine_id)
            medicine_details_list=[]
            for medicine_detail in request.data["medicine_details"]:
                #print(medicine_detail)

                #adding the medicine id which will work for the medicine id serializer
                medicine_detail["medicine_id"] = medicine_id
                medicine_details_list.append(medicine_detail)
                print(medicine_detail)

            serializer2=MedicalDetailsSerializer(data=medicine_details_list, many=True,context={"request":request})
            serializer2.is_valid()
            serializer2.save()
            dict_response={"error":False,"message":"Medicine Data Saved Successfully"}
        except:
            dict_response={"error":True,"message":"Error while Saving Medicine Data"}
        return Response(dict_response)
    
    def list(self,request):
        medicine=Medicine.objects.all()
        serializer=MedicineSerliazer(medicine,many=True, context={"request", request})

        medicine_data=serializer.data
        newmedicinelist=[]

        for medicine in medicine_data:
            medicine_details=MedicalDetails.objects.filter(medicine_id=medicine["id"])
            medicine_details_serializers=MedicalDetailsSerializerSimple(medicine_details,many=True)
            medicine["medicine_details"]=medicine_details_serializers.data
            newmedicinelist.append(medicine)

        
        response_dict={"error": False, "message": "All Medicine List Data", "data":newmedicinelist}
        return Response(response_dict)    
    
    def retrieve(self, request, pk=None):
        queryset=Medicine.objects.all()
        medicine=get_object_or_404(queryset, pk=pk)
        serializer=MedicineSerliazer(medicine, context={"request":request})

        serializer_data=serializer.data
        medicine_details = MedicalDetails.objects.filter(medicine_id=serializer_data["id"])
        medicine_details_serializer=MedicalDetailsSerializerSimple(medicine_details, many=True)
        serializer_data['medicine_details'] = medicine_details_serializer.data


        return Response({"error":False, "message": "single data fetched", "data":serializer.data})

    def update(self, request, pk=None):
        queryset=Medicine.objects.all()
        companybank=get_object_or_404(queryset, pk=pk)
        serializer=MedicineSerliazer(companybank,data=request.data, context={"request":request})
        serializer.is_valid()
        serializer.save()
        return Response({"error":False, "message":"Data has been Updated"})
 

company_list=CompanyViewSet.as_view({"get":"list"})
company_create=CompanyViewSet.as_view({"post":"create"})
company_update=CompanyViewSet.as_view({"put":"update"})
#company_bank_create=CompanyBankViewset({'post':"create"})
