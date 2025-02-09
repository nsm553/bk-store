import strawberry

@strawberry.type
class BusinessInfo():
    name = str
    description = str
    revenue = float

@strawberry.type
class Query():
    @strawberry.field
    def business_info(self, name: str) -> BusinessInfo:
        # Logic to fetch business information based on the name
        # This is a placeholder implementation
        return BusinessInfo(name=name, description="Sample business", revenue=100000.0)

schema = strawberry.Schema(query=Query)