import SignIn from './screens/SignIn';
import SignUp from './screens/SignUp';
import Splash from './screens/Splash';
import Home from './screens/Home';
import LightShapeScreen from './screens/LightShapeScreen';
import BluetoothPage from './screens/BluetoothPage';
//import Tabs from './navigation/Tabs';
//import MainContainer from './screens/MainContainer';
import { StyleSheet, Text, View } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

const Stack = createNativeStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator
        screenOptions={{
        headerShown: false
      }}
      >
        <Stack.Screen
          name="Splash"
          component={Splash}
          
        />
        <Stack.Screen
          name="SignIn"
          component={SignIn}
        />
        <Stack.Screen
          name="SignUp"
          component={SignUp}
         />
         <Stack.Screen
          name="Home"
          component={Home}
         >
         </Stack.Screen>
         <Stack.Screen
          name="LightShape"
          component={LightShapeScreen}
         >
         </Stack.Screen>
         <Stack.Screen
          name="Bluetooth"
          component={BluetoothPage}
         >
         </Stack.Screen>
         
      </Stack.Navigator>
    </NavigationContainer>
  );
}


