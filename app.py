from constructs import Construct
from aws_cdk import (
    App, Stack,
    aws_lambda as _lambda,
    aws_apigateway as _apigw
)


class ApiCorsLambdaStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        calculate_distance_lambda = _lambda.Function(self, 'ApiDistanceLambda',
                                       handler='distance-lambda-handler.handler',
                                       runtime=_lambda.Runtime.PYTHON_3_7,
                                       code=_lambda.Code.from_asset('lambda'))

        calculate_distance_api = _apigw.RestApi(self, 'DistanceApiGatewayWithCors',
                                  rest_api_name='DistanceApiGatewayWithCors')

        distance_entity = calculate_distance_api.root.add_resource(
            'distance',
            default_cors_preflight_options=_apigw.CorsOptions(
                allow_methods=['GET', 'OPTIONS'],
                allow_origins=_apigw.Cors.ALL_ORIGINS)
        )
        distance_entity_lambda_integration = _apigw.LambdaIntegration(
            calculate_distance_lambda,
            proxy=False,
            integration_responses=[
                _apigw.IntegrationResponse(
                    status_code="200",
                    response_parameters={
                        'method.response.header.Access-Control-Allow-Origin': "'*'"
                    }
                )
            ]
        )
        distance_entity.add_method(
            'GET', distance_entity_lambda_integration,
            method_responses=[
                _apigw.MethodResponse(
                    status_code="200",
                    response_parameters={
                        'method.response.header.Access-Control-Allow-Origin': True
                    }
                )
            ]
        )


        """ Assuming we charge 1.5$ per kilometer, 1.2$ per minute, base fair for each trip is 2$
         and formula for caluclation for each trip we are assuming is:
         total_price = ( (price_per_km * 1) + (price_per_minute *1.5) + base_fair ) / distance """

        price_per_km = 1.5
        price_per_minute = 1.5
        base_fair = 2
        # Get Distance by calling distance lambda
        distance = 8


        # calculate_price_lambda = _lambda.Function(self, 'ApiPriceLambda',
        #                                handler='price-lambda-handler.handler',
        #                                runtime=_lambda.Runtime.PYTHON_3_7,
        #                                code=_lambda.Code.from_asset('lambda'),
        #                                environment={
        #                                 'PRICE_PER_KM': str(price_per_km),
        #                                 'PRICE_PER_DISTANCE': str(price_per_km),
        #                                 'BASE_FAIR': str(base_fair),
        #                                 'DISTANCE': str(distance),
        #                                 }
        # )
        

        calculate_price_lambda = _lambda.Function(self, 'ApiPriceLambda',
                                       handler='price-lambda-handler.handler',
                                       runtime=_lambda.Runtime.PYTHON_3_7,
                                       code=_lambda.Code.from_asset('lambda'),)
        calculate_price_lambda.add_environment(
            'PRICE_PER_KM', str(price_per_km)
        )

        calculate_price_lambda.add_environment(
            'PRICE_PER_MINUTE', str(price_per_minute)
        )
        calculate_price_lambda.add_variable(
            'BASE_FAIR', str(base_fair)
        )
        calculate_price_lambda.add_variable(
            'DISTANCE', str(distance)
        )
        
        calculate_price_api = _apigw.RestApi(self, 'PriceApiGatewayWithCors',
                                  rest_api_name='PriceApiGatewayWithCors')

        price_entity = calculate_price_api.root.add_resource(
            'price',
            default_cors_preflight_options=_apigw.CorsOptions(
                allow_methods=['GET', 'OPTIONS'],
                allow_origins=_apigw.Cors.ALL_ORIGINS)
        )
        price_entity_lambda_integration = _apigw.LambdaIntegration(
            calculate_price_lambda,
            proxy=False,
            integration_responses=[
                _apigw.IntegrationResponse(
                    status_code="200",
                    response_parameters={
                        'method.response.header.Access-Control-Allow-Origin': "'*'"
                    }
                )
            ]
        )
        price_entity.add_method(
            'GET', price_entity_lambda_integration,
            method_responses=[
                _apigw.MethodResponse(
                    status_code="200",
                    response_parameters={
                        'method.response.header.Access-Control-Allow-Origin': True
                    }
                )
            ]
        )


app = App()
ApiCorsLambdaStack(app, "ApiCorsLambdaStack")
app.synth()
