//
//  SocketIOClient+SendMessage.swift
//  MobiliumDriver
//
//  Created by Grzegorz Przybyła on 16/09/2019.
//  Copyright © 2019 Silvair. All rights reserved.
//

import Foundation
import SocketIO
extension SocketIOClient {
    
    func send(message data: Data) {
        emit("message", with: [data])
    }
}
